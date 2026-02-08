from typing import Dict, Any
from sqlmodel import Session, select
from models import Task
from db import engine


def update_task(user_id: str, task_id: int, title: str = None, description: str = None, completed: bool = None) -> Dict[str, Any]:
    """
    Update an existing task for the authenticated user.

    Args:
        user_id: The ID of the user requesting the operation
        task_id: The ID of the task to update
        title: Optional new title for the task
        description: Optional new description for the task
        completed: Optional new completion status for the task

    Returns:
        Dictionary containing the updated task information
    """
    with Session(engine) as session:
        # First, get the task to ensure it belongs to the user
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            return {
                "success": False,
                "message": f"Task with ID {task_id} not found or does not belong to you"
            }

        # Update the task with provided values
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            },
            "message": f"Task '{task.title}' has been updated successfully"
        }