from typing import Dict, Any, Optional
from sqlmodel import Session, select
from uuid import UUID
from ..models.conversation import Conversation
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from db import engine


def create_conversation(user_id: str) -> Dict[str, Any]:
    """
    Create a new conversation for the authenticated user.

    Args:
        user_id: The ID of the user requesting the operation

    Returns:
        Dictionary containing the created conversation information
    """
    with Session(engine) as session:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        return {
            "success": True,
            "conversation": {
                "id": str(conversation.id),
                "user_id": conversation.user_id,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat()
            },
            "message": "Conversation created successfully"
        }


def get_conversation(conversation_id: UUID, user_id: str) -> Dict[str, Any]:
    """
    Retrieve a specific conversation for the authenticated user.

    Args:
        conversation_id: The ID of the conversation to retrieve
        user_id: The ID of the user requesting the operation

    Returns:
        Dictionary containing the conversation information
    """
    with Session(engine) as session:
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(statement).first()

        if not conversation:
            return {
                "success": False,
                "message": "Conversation not found or access denied"
            }

        return {
            "success": True,
            "conversation": {
                "id": str(conversation.id),
                "user_id": conversation.user_id,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat()
            }
        }


def get_user_conversations(user_id: str) -> Dict[str, Any]:
    """
    Retrieve all conversations for the authenticated user.

    Args:
        user_id: The ID of the user requesting the operation

    Returns:
        Dictionary containing the list of conversations
    """
    with Session(engine) as session:
        statement = select(Conversation).where(Conversation.user_id == user_id)
        conversations = session.exec(statement).all()

        conversation_list = []
        for conv in conversations:
            conversation_list.append({
                "id": str(conv.id),
                "user_id": conv.user_id,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat()
            })

        return {
            "success": True,
            "conversations": conversation_list,
            "count": len(conversation_list)
        }