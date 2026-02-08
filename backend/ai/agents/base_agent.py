from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..services.cohere_client import CohereClientWrapper
from ..models.conversation import Conversation
from ..models.message import Message


class BaseAgent(ABC):
    """
    Base agent class that manages the conversation state and orchestrates
    interactions with tools using Cohere as the underlying LLM.
    """

    def __init__(self, cohere_client: CohereClientWrapper):
        self.cohere_client = cohere_client

    @abstractmethod
    def process_message(self, conversation: Conversation, user_message: Message) -> str:
        """
        Process a user message and return an agent response.
        """
        pass

    @abstractmethod
    def get_conversation_context(self, conversation_id: str) -> List[Dict[str, str]]:
        """
        Get the conversation context for a given conversation ID.
        """
        pass

    def format_conversation_for_llm(self, messages: List[Message]) -> List[Dict[str, str]]:
        """
        Format conversation messages for LLM consumption.
        """
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                "role": msg.role.value if hasattr(msg.role, 'value') else msg.role,
                "content": msg.content
            })
        return formatted_messages