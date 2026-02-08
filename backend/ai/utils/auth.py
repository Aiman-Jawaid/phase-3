from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWTError
from pydantic import BaseModel


security = HTTPBearer()


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[str] = None


def extract_user_id_from_jwt(token: str, secret_key: str) -> Optional[str]:
    """
    Extract user_id from JWT token.
    This function assumes that the JWT contains a 'user_id' claim.
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials: Missing user_id"
            )

        return user_id
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials: Invalid token"
        )


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to get the current user ID from the JWT token.
    This is a placeholder that assumes you have a SECRET_KEY configured.
    In a real implementation, you'd get this from your config.
    """
    # In a real implementation, you would get the secret from your config
    # For now, we'll use a placeholder - this should be replaced with actual secret management
    SECRET_KEY = "your-secret-key-here"  # This should come from config in real implementation

    token = credentials.credentials
    return extract_user_id_from_jwt(token, SECRET_KEY)