from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    """
    Schema for creating a new task
    """
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    """
    Schema for task response with all fields
    """
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskToggleComplete(BaseModel):
    """
    Schema for toggling task completion status
    """
    completed: bool


class TokenData(BaseModel):
    """
    Schema for JWT token data
    """
    user_id: Optional[str] = None


class TaskFilterParams(BaseModel):
    """
    Schema for task filtering parameters
    """
    status: Optional[str] = None  # all, pending, completed