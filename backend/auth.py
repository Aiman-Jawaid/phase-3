from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from models import pwd_context

# Load environment variables
load_dotenv()

# Initialize security scheme for JWT in headers
security = HTTPBearer()

# Get secret from environment
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback_secret_for_development")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TokenData(BaseModel):
    user_id: Optional[str] = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    """
    # Check if this is a SHA256 hash with salt (our fallback format: $SHA256$salt$hash)
    if hashed_password.startswith("$SHA256$"):
        try:
            import hashlib
            parts = hashed_password.split("$")
            if len(parts) >= 4:
                _, algo, salt, stored_hash = parts[0], parts[1], parts[2], parts[3]
                
                # Create MD5 digest of the plain password first (to match our hashing approach)
                password_digest = hashlib.md5(plain_password.encode('utf-8')).hexdigest()
                
                # Combine with salt and hash
                salted_password = password_digest + salt
                computed_hash = hashlib.sha256(salted_password.encode()).hexdigest()
                
                return computed_hash == stored_hash
        except:
            return False
    
    try:
        # First, try normal verification
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        # Log the error for debugging purposes
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Password verification error: {str(e)}")

        # If it's a known bcrypt issue, try with a truncated version of the plain password
        if "password cannot be longer than 72 bytes" in str(e):
            # Truncate the plain password the same way we do during hashing (with safety margin)
            truncated_plain = plain_password[:50]
            truncated_bytes = truncated_plain.encode('utf-8')
            if len(truncated_bytes) > 72:
                truncated_plain = truncated_bytes[:50].decode('utf-8', errors='ignore')

            try:
                return pwd_context.verify(truncated_plain, hashed_password)
            except:
                # If that also fails, try with the hash approach (for passwords stored using the fallback)
                import hashlib
                password_digest = hashlib.md5(plain_password.encode('utf-8')).hexdigest()
                try:
                    return pwd_context.verify(password_digest, hashed_password)
                except:
                    return False

        return False


def get_password_hash(password: str) -> str:
    """
    Hash a plain password
    """
    # Pre-validate password length to ensure it's under 72 bytes
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 50 bytes to leave significant safety margin and decode back to string
        password = password_bytes[:50].decode('utf-8', errors='ignore')

    # Also ensure character length is within bounds (using a conservative limit)
    if len(password) > 50:
        password = password[:50]

    try:
        return pwd_context.hash(password)
    except ValueError as e:
        if "password cannot be longer than 72 bytes" in str(e):
            # If the error still occurs, use a deterministic approach with a much shorter string
            import hashlib
            # Create a MD5 hash of the original password (always 32 characters)
            # This is well under the 72-byte limit and should definitely work with bcrypt
            password_digest = hashlib.md5(password.encode('utf-8')).hexdigest()
            try:
                return pwd_context.hash(password_digest)
            except:
                # If bcrypt still fails, use a pure hashlib approach as last resort
                # Note: This is less secure but will work when bcrypt is unavailable
                import hashlib
                import secrets
                salt = secrets.token_hex(16)  # 16 bytes = 32 hex chars
                salted_password = password_digest + salt
                hashed = hashlib.sha256(salted_password.encode()).hexdigest()
                # Store salt with hash for verification
                return f"$SHA256${salt}${hashed}"
        else:
            raise e


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """
    Verify JWT token and extract user_id from the 'sub' claim
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(user_id=user_id)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Get current user from JWT token in Authorization header
    Returns user_id extracted from JWT 'sub' claim
    """
    token = credentials.credentials
    token_data = verify_token(token)

    if token_data.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return token_data.user_id