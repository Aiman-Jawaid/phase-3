import cohere
from typing import Dict, List, Any
from ..config import ai_config
import logging

logger = logging.getLogger(__name__)


class CohereClientWrapper:
    """
    Cohere client wrapper that adapts to work with OpenAI Agents SDK patterns.
    Formats responses to be compatible with the agent orchestration system.
    """

    def __init__(self):
        if not ai_config.cohere_api_key:
            logger.warning("COHERE_API_KEY environment variable is not set - AI features will use fallback responses")
            self.client = None
        else:
            try:
                self.client = cohere.Client(api_key=ai_config.cohere_api_key)
                # Test the connection - use a minimal test to avoid errors
                # Don't actually call the API during initialization to avoid network issues
            except Exception as e:
                logger.error(f"Failed to initialize Cohere client: {str(e)}")
                logger.warning("AI features will use fallback responses")
                self.client = None

    def generate_response(self, conversation_history: List[Dict[str, str]], user_input: str) -> str:
        """
        Generate a response based on conversation history and user input.
        """
        if not self.client:
            # Fallback response when Cohere is not available
            return self._get_fallback_response(user_input, "generate_response")
            
        try:
            # Format the conversation history for Cohere
            formatted_history = []
            for msg in conversation_history:
                role = msg.get('role', 'user')
                message = msg.get('content', '')

                formatted_history.append({
                    "user_name": role,
                    "text": message
                })

            # Create a prompt combining the history and new user input
            history_text = "\n".join([f"{msg['user_name']}: {msg['text']}" for msg in formatted_history])
            full_prompt = f"{history_text}\nuser: {user_input}\nassistant:"

            # Generate response using Cohere
            response = self.client.generate(
                model='command',
                prompt=full_prompt,
                max_tokens=500,
                temperature=0.7
            )

            return response.generations[0].text.strip()
        except ConnectionError as e:
            logger.error(f"Connection error with Cohere API: {str(e)}")
            return "Sorry, I'm unable to connect to the AI service right now. Please try again later."
        except TimeoutError as e:
            logger.error(f"Timeout error with Cohere API: {str(e)}")
            return "The AI service is taking too long to respond. Please try again later."
        except Exception as e:
            logger.error(f"Cohere API error: {str(e)}")
            if "API key" in str(e) or "authentication" in str(e).lower():
                return "There's an issue with the AI service configuration. Please contact support."
            return "Sorry, I'm experiencing technical difficulties. Please try again later."

    def _get_fallback_response(self, user_input: str, method: str = "chat") -> str:
        """
        Provide intelligent fallback responses when Cohere API is unavailable.
        """
        user_input_lower = user_input.lower().strip()
        
        # Simple pattern matching for common queries
        if any(greeting in user_input_lower for greeting in ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]):
            return "Hello! I'm your AI Todo Assistant. I can help you manage your tasks. You can ask me to add, list, complete, or delete tasks. How can I assist you today?"
        elif any(query in user_input_lower for query in ["help", "what can you do", "how do i", "instructions", "commands"]):
            return "I can help you manage your tasks! You can ask me to:\n- Add a task (e.g., 'Add a task to buy groceries')\n- List your tasks (e.g., 'Show my tasks')\n- Complete a task (e.g., 'Mark task 1 as complete')\n- Update a task (e.g., 'Change task 1 to walk the dog')\n- Delete a task (e.g., 'Delete task 1')"
        elif any(query in user_input_lower for query in ["what", "list", "show", "my tasks", "tasks"]):
            return "I'd be happy to list your tasks, but I need to connect to the AI service to do that. Please make sure you have a valid API key configured."
        elif any(query in user_input_lower for query in ["add", "create", "new task"]):
            return "I can help you add a task! Please provide a clear description of the task you'd like to add."
        elif any(query in user_input_lower for query in ["complete", "done", "finish"]):
            return "I can help you mark a task as complete. Please specify which task number you'd like to mark as complete."
        else:
            return "I understand you're saying '" + user_input + "'. I'm your AI Todo Assistant, but I'm currently having trouble connecting to my AI services. I can still help you manage your tasks once connectivity is restored. Is there a specific task you'd like to add, list, update, or complete?"

    def chat(self, message: str, conversation_id: str = None, preamble: str = None) -> Dict[str, Any]:
        """
        Perform a chat interaction with the Cohere model.
        """
        if not self.client:
            # Fallback response when Cohere is not available
            return {
                "text": self._get_fallback_response(message, "chat"),
                "conversation_id": conversation_id or "",
                "meta": {"error": "cohere_unavailable", "fallback_used": True}
            }
        
        try:
            response = self.client.chat(
                message=message,
                conversation_id=conversation_id,
                preamble=preamble
            )

            return {
                "text": response.text,
                "conversation_id": response.conversation_id,
                "meta": response.meta
            }
        except ConnectionError as e:
            logger.error(f"Connection error with Cohere API during chat: {str(e)}")
            return {
                "text": "Sorry, I'm unable to connect to the AI service right now. Please try again later.",
                "conversation_id": conversation_id,
                "meta": {"error": "connection_error"}
            }
        except TimeoutError as e:
            logger.error(f"Timeout error with Cohere API during chat: {str(e)}")
            return {
                "text": "The AI service is taking too long to respond. Please try again later.",
                "conversation_id": conversation_id,
                "meta": {"error": "timeout_error"}
            }
        except Exception as e:
            logger.error(f"Cohere API error during chat: {str(e)}")
            if "API key" in str(e) or "authentication" in str(e).lower():
                return {
                    "text": "There's an issue with the AI service configuration. Please contact support.",
                    "conversation_id": conversation_id,
                    "meta": {"error": "auth_error"}
                }
            return {
                "text": "Sorry, I'm experiencing technical difficulties. Please try again later.",
                "conversation_id": conversation_id,
                "meta": {"error": str(e)}
            }