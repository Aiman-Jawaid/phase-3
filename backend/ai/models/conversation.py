from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class ConversationBase(SQLModel):
    user_id: str = Field(index=True)  # Reference to the user who owns this conversation


class Conversation(ConversationBase, table=True):
    """
    Represents a chat session between a user and the AI assistant,
    containing metadata about the conversation and linking to associated messages.
    """
    __tablename__ = "conversation"  # Explicitly set table name to avoid conflicts
    __table_args__ = {"extend_existing": True}  # Allow extending if already defined

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime