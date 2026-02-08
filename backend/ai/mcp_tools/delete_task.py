from typing import Dict, Any
from sqlmodel import Session, select
from models import Task
from db import engine


def delete_task(user_id: str, task_id: int, confirmed: bool = False) -> Dict[str, Any]:
    """
    Delete a task for the authenticated user.

    Args:
        user_id: The ID of the user requesting the operation
        task_id: The ID of the task to delete
        confirmed: Whether the user has confirmed the destructive operation

    Returns:
        Dictionary containing the result of the operation
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

        # If not confirmed, return a confirmation message instead of deleting
        if not confirmed:
            return {
                "success": False,
                "requires_confirmation": True,
                "message": f"Are you sure you want to delete task '{task.title}'? This action cannot be undone. Please confirm the deletion.",
                "task_title": task.title
            }

        # User has confirmed, proceed with deletion
        session.delete(task)
        session.commit()

        return {
            "success": True,
            "message": f"Task '{task.title}' has been deleted successfully"
        }