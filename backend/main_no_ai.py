from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Validate required environment variables
def validate_environment():
    required_vars = ["BETTER_AUTH_SECRET", "DATABASE_URL"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

validate_environment()

# Import database and create tables first to avoid conflicts
from backend.db import engine
from sqlmodel import SQLModel

# Import models to register them with SQLModel metadata
from backend.models import Task
# Note: We're not importing AI models here to avoid Python 3.14 compatibility issues

# Import exception handlers
from backend.utils.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Create database tables on startup
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app instance
app = FastAPI(
    title="Todo API",
    description="Secure Todo Management Backend with JWT Authentication",
    version="1.0.0"
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "https://localhost:3000", "https://127.0.0.1:3000"],  # Frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Authorization", "Content-Type"],  # Allow all headers plus auth and content-type
)

# Register custom exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Todo API - Secure Todo Management Backend"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-backend"}

# Include routes after app is initialized (excluding chat route to avoid AI dependencies)
def include_routes():
    from backend.routes import tasks, auth  # Exclude chat route
    app.include_router(tasks.router, prefix="/api", tags=["tasks"])
    app.include_router(auth.router, prefix="/api", tags=["auth"])

include_routes()