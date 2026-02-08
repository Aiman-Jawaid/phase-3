from typing import Dict, Any, List
from .base_agent import BaseAgent
from .intent_detector import IntentDetector
from ..services.task_service import TaskOrchestrationService
from ..services.cohere_client import CohereClientWrapper
from ..services.conversation_service import get_conversation
from ..services.message_service import get_conversation_messages, create_message
from uuid import UUID


class ChatAgent(BaseAgent):
    """
    Chat agent that manages task management conversations using natural language.
    """

    def __init__(self, cohere_client: CohereClientWrapper, task_service: TaskOrchestrationService):
        super().__init__(cohere_client)
        self.task_service = task_service
        self.intent_detector = IntentDetector()
        # Track pending confirmations for destructive operations
        self.pending_confirmations = {}

    def process_message(self, user_id: str, conversation_id: str, user_message: str) -> str:
        """
        Process a user message and return an agent response.

        Args:
            user_id: The ID of the authenticated user
            conversation_id: The ID of the conversation
            user_message: The message from the user

        Returns:
            The agent's response
        """
        try:
            # Get conversation context if conversation_id is provided
            context_messages = []
            if conversation_id:
                context_messages = self.get_conversation_context(conversation_id, user_id)

            # Check if this is a confirmation for a pending destructive operation
            user_message_lower = user_message.lower().strip()
            confirmation_keywords = ["yes", "confirm", "ok", "okay", "sure", "delete", "go ahead", "proceed"]

            # Check if user is confirming a pending operation
            pending_key = f"{user_id}:{conversation_id}" if conversation_id else user_id
            if pending_key in self.pending_confirmations and any(keyword in user_message_lower for keyword in confirmation_keywords):
                # Retrieve the pending operation details
                pending_op = self.pending_confirmations[pending_key]
                del self.pending_confirmations[pending_key]  # Clear the pending confirmation

                # Execute the confirmed operation
                result = self.task_service.execute_task_operation(
                    user_id,
                    pending_op["operation"],
                    task_id=pending_op["task_id"],
                    confirmed=True
                )

                # Format the response based on the result
                if result["success"]:
                    if "message" in result:
                        return result["message"]
                    else:
                        return "Operation completed successfully."
                else:
                    return f"Error: {result.get('message', 'Unknown error occurred')}"

            # Detect the intent from the user message
            intent_result = self.intent_detector.detect_intent(user_message, context_messages)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in process_message before intent processing: {str(e)}")
            
            # Provide fallback response for any errors during processing
            user_message_lower = user_message.lower().strip()
            if any(greeting in user_message_lower for greeting in ["hello", "hi", "hey", "greetings"]):
                return "Hello! I'm your AI Todo Assistant. I can help you manage your tasks. You can ask me to add, list, complete, or delete tasks. How can I assist you today?"
            elif any(query in user_message_lower for query in ["help", "what can you do", "how do i"]):
                return "I can help you manage your tasks! You can ask me to add, list, complete, update, or delete tasks. For example: 'Add a task to buy groceries' or 'Show my tasks'."
            else:
                return "I'm currently experiencing technical difficulties with my AI services, but I'm still here to help. You can ask me to add, list, complete, update, or delete tasks when I'm back online."

        # Check if this is a confirmation intent and we have a pending operation
        if intent_result["operation"] == "confirm_destructive_action":
            # Check if there's a pending operation for this user/conversation
            pending_key = f"{user_id}:{conversation_id}" if conversation_id else user_id
            if pending_key in self.pending_confirmations:
                pending_op = self.pending_confirmations[pending_key]
                del self.pending_confirmations[pending_key]  # Clear the pending confirmation

                # Execute the confirmed operation
                result = self.task_service.execute_task_operation(
                    user_id,
                    pending_op["operation"],
                    task_id=pending_op["task_id"],
                    confirmed=True
                )

                # Format the response based on the result
                if result["success"]:
                    if "message" in result:
                        return result["message"]
                    else:
                        return "Operation completed successfully."
                else:
                    return f"Error: {result.get('message', 'Unknown error occurred')}"

        if intent_result["operation"] == "unknown":
            # If the intent is unknown, use the LLM to generate a response
            # Include conversation context if available
            if not self.cohere_client or not self.cohere_client.client:  # Check if Cohere client is available
                # Use fallback response when Cohere is not available
                user_message_lower = user_message.lower().strip()
                if any(greeting in user_message_lower for greeting in ["hello", "hi", "hey", "greetings"]):
                    return "Hello! I'm your AI Todo Assistant. I can help you manage your tasks. You can ask me to add, list, complete, or delete tasks. How can I assist you today?"
                elif any(query in user_message_lower for query in ["help", "what can you do", "how do i"]):
                    return "I can help you manage your tasks! You can ask me to add, list, complete, update, or delete tasks. For example: 'Add a task to buy groceries' or 'Show my tasks'."
                else:
                    return "I'm currently experiencing technical difficulties with my AI services, but I'm still here to help. You can ask me to add, list, complete, update, or delete tasks when I'm back online."
            
            if context_messages:
                # Build a context-aware prompt with conversation history
                context_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in context_messages[-5:]])  # Last 5 messages
                enhanced_prompt = f"Conversation context:\n{context_str}\n\nCurrent user message: {user_message}"
                llm_response = self.cohere_client.chat(enhanced_prompt)
            else:
                llm_response = self.cohere_client.chat(user_message)
            return llm_response["text"]

        # Execute the appropriate task operation based on the detected intent
        operation = intent_result["operation"]
        params = intent_result.get("params", {})

        # Add user_id to the parameters
        params["user_id"] = user_id

        # Execute the operation
        result = self.task_service.execute_task_operation(user_id, operation, **params)

        # Handle confirmation for destructive operations (like delete_task)
        if result.get("requires_confirmation"):
            # Store the operation details for confirmation
            pending_key = f"{user_id}:{conversation_id}" if conversation_id else user_id
            self.pending_confirmations[pending_key] = {
                "operation": operation,
                "task_id": params.get("task_id"),
                "original_message": user_message
            }
            # This indicates a destructive operation that needs confirmation
            return result["message"]

        # Format the response based on the result
        if result["success"]:
            if "message" in result:
                return result["message"]
            elif "tasks" in result:
                if len(result["tasks"]) == 0:
                    return "You don't have any tasks matching that criteria."
                else:
                    task_list = []
                    for task in result["tasks"]:
                        status = "✓" if task["completed"] else "○"
                        task_list.append(f"{status} {task['id']}. {task['title']}")
                    return f"Here are your tasks:\n" + "\n".join(task_list)
            else:
                return "Operation completed successfully."
        else:
            return f"Error: {result.get('message', 'Unknown error occurred')}"

    def get_conversation_context(self, conversation_id: str, user_id: str) -> List[Dict[str, str]]:
        """
        Get the conversation context for a given conversation ID.

        Args:
            conversation_id: The ID of the conversation
            user_id: The ID of the authenticated user

        Returns:
            List of messages in the conversation for context
        """
        try:
            # Get the conversation to ensure it exists and belongs to the user
            conv_result = get_conversation(UUID(conversation_id), user_id)
            if not conv_result["success"]:
                return []

            # Get all messages in the conversation
            messages_result = get_conversation_messages(UUID(conversation_id), user_id)
            if not messages_result["success"]:
                return []

            # Format messages for context
            context_messages = []
            for msg in messages_result["messages"]:
                context_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

            return context_messages
        except Exception:
            # If there's an error (e.g., invalid UUID), return empty context
            return []

    def handle_natural_language_request(self, user_id: str, user_message: str, conversation_id: str = "") -> Dict[str, Any]:
        """
        Handle a natural language request from a user.

        Args:
            user_id: The ID of the authenticated user
            user_message: The user's natural language request
            conversation_id: Optional conversation ID for context

        Returns:
            Dictionary containing the agent's response and any tool calls
        """
        try:
            # Process the message and get the response
            response_text = self.process_message(user_id, conversation_id, user_message)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in chat agent processing: {str(e)}")
            
            # Provide a fallback response when processing fails
            user_input_lower = user_message.lower().strip()
            if any(greeting in user_input_lower for greeting in ["hello", "hi", "hey", "greetings"]):
                response_text = "Hello! I'm your AI Todo Assistant. I can help you manage your tasks. You can ask me to add, list, complete, or delete tasks. How can I assist you today?"
            elif any(query in user_input_lower for query in ["help", "what can you do", "how do i"]):
                response_text = "I can help you manage your tasks! You can ask me to add, list, complete, update, or delete tasks. For example: 'Add a task to buy groceries' or 'Show my tasks'."
            else:
                response_text = "I'm currently experiencing technical difficulties with my AI services, but I'm still here to help. You can ask me to add, list, complete, update, or delete tasks when I'm back online."

        # For now, we'll return a simple response
        # In a more advanced implementation, we'd track which tools were called
        return {
            "response": response_text,
            "tool_calls": []  # This would be populated with actual tool calls in a more advanced implementation
        }