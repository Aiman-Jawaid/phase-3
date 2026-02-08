from typing import Dict, Any
from sqlmodel import Session, select
from models import Task, TaskCreate
from db import engine


def add_task(user_id: str, title: str, description: str = None) -> Dict[str, Any]:
    """
    Add a new task for the authenticated user.

    Args:
        user_id: The ID of the user requesting the operation
        title: The title of the task to add
        description: Optional description of the task

    Returns:
        Dictionary containing the created task information
    """
    task_create = TaskCreate(title=title, description=description, completed=False)

    with Session(engine) as session:
        task = Task(
            user_id=user_id,
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed
        )
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
            "message": f"Task '{task.title}' has been added successfully"
        }