from typing import Dict, Any, List
from sqlmodel import Session, select
from models import Task
from db import engine


def list_tasks(user_id: str, status: str = None) -> Dict[str, Any]:
    """
    List tasks for the authenticated user, with optional status filtering.

    Args:
        user_id: The ID of the user requesting the operation
        status: Optional status filter ('pending', 'completed', or None for all)

    Returns:
        Dictionary containing the list of tasks
    """
    with Session(engine) as session:
        query = select(Task).where(Task.user_id == user_id)

        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        tasks = session.exec(query).all()

        task_list = []
        for task in tasks:
            task_list.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            })

        status_desc = f" ({status})" if status else ""
        return {
            "success": True,
            "tasks": task_list,
            "count": len(task_list),
            "message": f"You have {len(task_list)} task{status_desc}{'' if len(task_list) == 1 else 's'}"
        }