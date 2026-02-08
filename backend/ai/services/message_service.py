from typing import Dict, Any, List
from sqlmodel import Session, select
from uuid import UUID
from ..models.message import Message
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from db import engine


def create_message(conversation_id: UUID, user_id: str, role: str, content: str) -> Dict[str, Any]:
    """
    Create a new message in a conversation.

    Args:
        conversation_id: The ID of the conversation to add the message to
        user_id: The ID of the user who sent the message
        role: The role of the message sender ("user" or "assistant")
        content: The content of the message

    Returns:
        Dictionary containing the created message information
    """
    with Session(engine) as session:
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content
        )
        session.add(message)
        session.commit()
        session.refresh(message)

        return {
            "success": True,
            "message": {
                "id": str(message.id),
                "conversation_id": str(message.conversation_id),
                "user_id": message.user_id,
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at.isoformat()
            },
            "message_text": "Message created successfully"
        }


def get_conversation_messages(conversation_id: UUID, user_id: str) -> Dict[str, Any]:
    """
    Retrieve all messages in a specific conversation for the authenticated user.

    Args:
        conversation_id: The ID of the conversation to retrieve messages from
        user_id: The ID of the user requesting the operation

    Returns:
        Dictionary containing the list of messages
    """
    with Session(engine) as session:
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())

        messages = session.exec(statement).all()

        # Verify that the user has access to this conversation by checking if any messages exist
        # (since messages are linked to conversations, if user can access messages in this convo,
        # they must have access to it)
        message_list = []
        for msg in messages:
            # Verify that the conversation belongs to the user by checking that at least one
            # message in the conversation belongs to the user
            if msg.user_id == user_id:
                message_list.append({
                    "id": str(msg.id),
                    "conversation_id": str(msg.conversation_id),
                    "user_id": msg.user_id,
                    "role": msg.role,
                    "content": msg.content,
                    "created_at": msg.created_at.isoformat()
                })

        # If no messages were accessible to the user, the conversation doesn't belong to them
        if not message_list and messages:  # If there are messages but none belong to the user
            return {
                "success": False,
                "message": "Access denied - conversation does not belong to user"
            }

        return {
            "success": True,
            "messages": message_list,
            "count": len(message_list)
        }


def get_latest_messages(conversation_id: UUID, user_id: str, limit: int = 10) -> Dict[str, Any]:
    """
    Retrieve the latest messages in a conversation for context.

    Args:
        conversation_id: The ID of the conversation to retrieve messages from
        user_id: The ID of the user requesting the operation
        limit: Number of recent messages to retrieve (default 10)

    Returns:
        Dictionary containing the list of recent messages
    """
    with Session(engine) as session:
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).limit(limit)

        messages = session.exec(statement).all()

        message_list = []
        for msg in messages:
            if msg.user_id == user_id:
                message_list.append({
                    "id": str(msg.id),
                    "conversation_id": str(msg.conversation_id),
                    "user_id": msg.user_id,
                    "role": msg.role,
                    "content": msg.content,
                    "created_at": msg.created_at.isoformat()
                })

        # Reverse the list to get chronological order (oldest first)
        message_list.reverse()

        if not message_list and messages:  # If there are messages but none belong to the user
            return {
                "success": False,
                "message": "Access denied - conversation does not belong to user"
            }

        return {
            "success": True,
            "messages": message_list,
            "count": len(message_list)
        }