from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid
from enum import Enum


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"


class MessageBase(SQLModel):
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", index=True)
    user_id: str = Field(index=True)  # Reference to the user who sent this message
    role: MessageRole  # Indicates whether the message was sent by user or assistant
    content: str = Field(max_length=5000)  # The actual content of the message


class Message(MessageBase, table=True):
    """
    Represents an individual message in a conversation, storing the content,
    sender (user or assistant), timestamp, and linking to the conversation and user.
    """
    __tablename__ = "message"  # Explicitly set table name to avoid conflicts
    __table_args__ = {"extend_existing": True}  # Allow extending if already defined

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: uuid.UUID
    created_at: datetime