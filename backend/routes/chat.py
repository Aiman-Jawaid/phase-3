from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, field_validator
from typing import Optional, List
from uuid import UUID
import json
from slowapi import Limiter
from slowapi.util import get_remote_address

from db import get_session
from sqlmodel import Session, select
from ai.models.conversation import Conversation
from ai.models.message import Message
from auth import get_current_user
from ai.agents.chat_agent import ChatAgent
from ai.services.cohere_client import CohereClientWrapper
from ai.services.task_service import TaskOrchestrationService
from ai.config import ai_config


# Initialize limiter for this module
limiter = Limiter(key_func=get_remote_address)
router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str

    @field_validator('message')
    @classmethod
    def validate_message(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Message cannot be empty')
        if len(v) > 2000:  # Limit message length to 2000 characters
            raise ValueError('Message must be less than 2000 characters')
        return v.strip()


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: List[str]


from fastapi import Request

@router.post("/chat", response_model=ChatResponse)
@limiter.limit("10/minute")  # Limit to 10 requests per minute per IP
async def chat(
    request: Request,  # This name is required for the rate limiter
    chat_request: ChatRequest,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Send a message to the AI chatbot and receive a response.
    The chatbot will interpret the natural language and perform appropriate task operations.
    Requires authentication via JWT token.
    """
    import time
    import logging

    # Start timing for performance monitoring
    start_time = time.time()
    logger = logging.getLogger(__name__)

    try:
        # Initialize AI components with error handling
        try:
            cohere_client = CohereClientWrapper()
            task_service = TaskOrchestrationService(cohere_client)
            chat_agent = ChatAgent(cohere_client, task_service)
        except Exception as init_error:
            logger.error(f"Error initializing AI components: {str(init_error)}")
            # Handle initialization error with fallback
            conversation = Conversation(user_id=current_user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

            # Create user message record
            user_message = Message(
                conversation_id=conversation.id,
                user_id=current_user_id,
                role="user",
                content=chat_request.message
            )
            session.add(user_message)
            session.commit()

            # Provide a fallback response
            user_input_lower = chat_request.message.lower().strip()
            if any(greeting in user_input_lower for greeting in ["hello", "hi", "hey", "greetings"]):
                fallback_response = "Hello! I'm your AI Todo Assistant. I can help you manage your tasks. You can ask me to add, list, complete, or delete tasks. How can I assist you today?"
            elif any(query in user_input_lower for query in ["help", "what can you do", "how do i"]):
                fallback_response = "I can help you manage your tasks! You can ask me to add, list, complete, update, or delete tasks. For example: 'Add a task to buy groceries' or 'Show my tasks'."
            else:
                fallback_response = "I'm currently experiencing technical difficulties with my AI services, but I'm still here to help. You can ask me to add, list, complete, update, or delete tasks when I'm back online."
            
            # Create assistant message record
            assistant_message = Message(
                conversation_id=conversation.id,
                user_id=current_user_id,
                role="assistant",
                content=fallback_response
            )
            session.add(assistant_message)
            session.commit()

            return ChatResponse(
                conversation_id=str(conversation.id),
                response=fallback_response,
                tool_calls=[]
            )

        # Create or retrieve conversation
        conversation = None
        if chat_request.conversation_id:
            # Try to find existing conversation
            stmt = select(Conversation).where(
                Conversation.id == UUID(chat_request.conversation_id),
                Conversation.user_id == current_user_id
            )
            conversation = session.exec(stmt).first()

        if not conversation:
            # Create new conversation if none exists or ID is invalid
            conversation = Conversation(user_id=current_user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        # Create user message record
        user_message = Message(
            conversation_id=conversation.id,
            user_id=current_user_id,
            role="user",
            content=chat_request.message
        )
        session.add(user_message)
        session.commit()

        # Process the message with the chat agent
        try:
            result = chat_agent.handle_natural_language_request(
                user_id=current_user_id,
                user_message=chat_request.message,
                conversation_id=str(conversation.id) if conversation else None
            )
        except Exception as e:
            logger.error(f"Error processing message with chat agent: {str(e)}")
            # Provide fallback response when chat agent fails
            user_input_lower = chat_request.message.lower().strip()
            if any(greeting in user_input_lower for greeting in ["hello", "hi", "hey", "greetings"]):
                fallback_response = "Hello! I'm your AI Todo Assistant. I can help you manage your tasks. You can ask me to add, list, complete, or delete tasks. How can I assist you today?"
            elif any(query in user_input_lower for query in ["help", "what can you do", "how do i"]):
                fallback_response = "I can help you manage your tasks! You can ask me to add, list, complete, update, or delete tasks. For example: 'Add a task to buy groceries' or 'Show my tasks'."
            else:
                fallback_response = "I'm currently experiencing technical difficulties with my AI services, but I'm still here to help. You can ask me to add, list, complete, update, or delete tasks when I'm back online."
            
            # Create assistant message record
            assistant_message = Message(
                conversation_id=conversation.id,
                user_id=current_user_id,
                role="assistant",
                content=fallback_response
            )
            session.add(assistant_message)
            session.commit()

            return ChatResponse(
                conversation_id=str(conversation.id),
                response=fallback_response,
                tool_calls=[]
            )

        # Create assistant message record
        assistant_message = Message(
            conversation_id=conversation.id,
            user_id=current_user_id,  # The assistant acts on behalf of the user
            role="assistant",
            content=result["response"]
        )
        session.add(assistant_message)
        session.commit()

        # Calculate response time for performance monitoring
        response_time = time.time() - start_time
        logger.info(f"Chat response time: {response_time:.2f}s for user {current_user_id}, conversation {conversation.id if conversation else 'new'}")

        return ChatResponse(
            conversation_id=str(conversation.id),
            response=result["response"],
            tool_calls=result.get("tool_calls", [])
        )

    except Exception as e:
        import traceback
        logger.error(f"Error processing chat request: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        
        # Return a more informative error or fallback response
        error_msg = str(e)
        if "cohere" in error_msg.lower() or "api" in error_msg.lower():
            # If it's an AI service error, provide a fallback response
            # Create a new conversation if needed
            conversation = None
            if chat_request.conversation_id:
                try:
                    from uuid import UUID
                    stmt = select(Conversation).where(
                        Conversation.id == UUID(chat_request.conversation_id),
                        Conversation.user_id == current_user_id
                    )
                    conversation = session.exec(stmt).first()
                except:
                    pass
            
            if not conversation:
                conversation = Conversation(user_id=current_user_id)
                session.add(conversation)
                session.commit()
                session.refresh(conversation)

            # Create user message record
            user_message = Message(
                conversation_id=conversation.id,
                user_id=current_user_id,
                role="user",
                content=chat_request.message
            )
            session.add(user_message)
            session.commit()

            # Provide a fallback response for common queries
            user_input_lower = chat_request.message.lower().strip()
            if any(greeting in user_input_lower for greeting in ["hello", "hi", "hey", "greetings"]):
                fallback_response = "Hello! I'm your AI Todo Assistant. I can help you manage your tasks. You can ask me to add, list, complete, or delete tasks. How can I assist you today?"
            elif any(query in user_input_lower for query in ["help", "what can you do", "how do i"]):
                fallback_response = "I can help you manage your tasks! You can ask me to add, list, complete, update, or delete tasks. For example: 'Add a task to buy groceries' or 'Show my tasks'."
            else:
                fallback_response = "I'm currently experiencing technical difficulties with my AI services, but I'm still here to help. You can ask me to add, list, complete, update, or delete tasks when I'm back online."
            
            # Create assistant message record
            assistant_message = Message(
                conversation_id=conversation.id,
                user_id=current_user_id,
                role="assistant",
                content=fallback_response
            )
            session.add(assistant_message)
            session.commit()

            return ChatResponse(
                conversation_id=str(conversation.id),
                response=fallback_response,
                tool_calls=[]
            )
        else:
            # For other errors, return the original error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing chat request: {str(e)}"
            )