from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime, timezone

from models import Task as TaskModel, TaskCreate as TaskCreateModel, TaskUpdate as TaskUpdateModel
from schemas import TaskResponse, TaskCreate, TaskUpdate, TaskToggleComplete
from db import get_session
from auth import get_current_user

# Create API router for task endpoints
router = APIRouter()


@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter tasks by status: all, pending, completed"),
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.
    Optionally filter by status: all, pending, completed
    """
    # Build query based on user_id and optional status filter
    query = select(TaskModel).where(TaskModel.user_id == current_user_id)

    if status_filter:
        if status_filter.lower() == "pending":
            query = query.where(TaskModel.completed == False)
        elif status_filter.lower() == "completed":
            query = query.where(TaskModel.completed == True)
        elif status_filter.lower() != "all":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status filter must be 'all', 'pending', or 'completed'"
            )

    tasks = session.exec(query).all()

    return tasks


@router.post("/tasks", response_model=TaskResponse)
def create_task(
    task_create: TaskCreate,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    The user_id is automatically set from the JWT token.
    """
    # Create task with user_id from JWT
    task = TaskModel(
        user_id=current_user_id,
        title=task_create.title,
        description=task_create.description,
        completed=False,  # Default to False for new tasks
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.
    Only returns tasks that belong to the authenticated user.
    """
    task = session.get(TaskModel, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Check if task belongs to current user
    if task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID.
    Only allows updating tasks that belong to the authenticated user.
    """
    task = session.get(TaskModel, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Check if task belongs to current user
    if task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update task fields if provided
    if task_update.title is not None:
        if len(task_update.title) < 1 or len(task_update.title) > 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title must be between 1 and 200 characters"
            )
        task.title = task_update.title

    if task_update.description is not None:
        task.description = task_update.description

    if task_update.completed is not None:
        task.completed = task_update.completed

    # Update the timestamp
    task.updated_at = datetime.now(timezone.utc)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion(
    task_id: int,
    task_toggle: TaskToggleComplete,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task.
    Only allows updating tasks that belong to the authenticated user.
    """
    task = session.get(TaskModel, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Check if task belongs to current user
    if task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update completion status
    task.completed = task_toggle.completed
    task.updated_at = datetime.now(timezone.utc)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(
    task_id: int,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID.
    Only allows deleting tasks that belong to the authenticated user.
    """
    task = session.get(TaskModel, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Check if task belongs to current user
    if task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()

    return {
        "message": "Task deleted successfully",
        "task_id": task_id
    }