from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel
from passlib.context import CryptContext
import uuid
from enum import Enum


# Initialize password context with bcrypt, with fallback options
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__rounds=12  # Specify bcrypt rounds explicitly to avoid version detection issues
)


def get_current_time():
    return datetime.now(timezone.utc)


class UserBase(SQLModel):
    """
    Base user model with email
    """
    email: str = Field(unique=True, nullable=False)
    name: str = Field(nullable=False)


class User(UserBase, table=True):
    """
    User model for authentication
    """
    __tablename__ = "user"  # Explicitly set table name to avoid conflicts
    __table_args__ = {"extend_existing": True}  # Allow extending if already defined

    id: Optional[str] = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)


class UserCreate(UserBase):
    """
    Model for creating new users
    """
    password: str = Field(min_length=6, max_length=50)  # Limit password to 50 characters to provide safety margin for bcrypt


class UserLogin(SQLModel):
    """
    Model for user login
    """
    email: str = Field(min_length=1)  # Ensure email is not empty
    password: str = Field(min_length=1, max_length=50)  # Ensure password is not empty and within bcrypt limits with safety margin


class UserPublic(UserBase):
    """
    Public user model without sensitive data
    """
    id: str
    created_at: datetime


class Token(SQLModel):
    """
    Token model for JWT authentication
    """
    access_token: str
    token_type: str = "bearer"


class Task(SQLModel, table=True):
    """
    Task model representing a todo item with title, description, completion status, and ownership.
    Attributes: id (auto-increment), user_id (foreign key reference), title (string),
    description (text), completed (boolean), created_at (timestamp), updated_at (timestamp).
    Each task belongs to exactly one user.
    """
    __tablename__ = "task"  # Explicitly set table name to avoid conflicts
    __table_args__ = {"extend_existing": True}  # Allow extending if already defined

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Indexed for performance
    title: str = Field(min_length=1, max_length=200)  # Required, 1-200 characters
    description: Optional[str] = Field(default=None)  # Optional
    completed: bool = Field(default=False)  # Defaults to False
    created_at: datetime = Field(default_factory=get_current_time)  # Auto-populated
    updated_at: datetime = Field(default_factory=get_current_time)  # Auto-populated


class TaskUpdate(SQLModel):
    """
    Model for updating task properties
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None)
    completed: Optional[bool] = Field(default=None)


class TaskCreate(SQLModel):
    """
    Model for creating new tasks
    """
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)


