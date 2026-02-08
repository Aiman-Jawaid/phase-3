import re
from typing import Dict, Any, Optional


class IntentDetector:
    """
    Detects user intent from natural language input and maps to appropriate MCP tools.
    """

    def __init__(self):
        # Define patterns for different intents
        self.patterns = {
            "add_task": [
                r"(?:add|create|make|new|add a|create a|make a|new)\s+(?:task|to-do|todo|item)\s+(?:to|for)?\s*(.+)",
                r"(?:add|create|make|new)\s+(.+)\s+(?:as a|as|to my)\s+(?:task|to-do|todo|item)",
                r"(?:remind me|remember|note|keep track of)\s+(.+)",
                r"(?:i need to|i have to|must|should)\s+(.+)",
            ],
            "list_tasks": [
                r"(?:show|list|display|get|fetch|see|view)\s+(?:my\s+)?(?:tasks|todos|to-dos|to dos|items|list)",
                r"(?:what|show|list|display|get|fetch|see|view)\s+(?:have i got|do i have|are my|is my|are there any|is there any)\s*(?:pending|completed|done|all)?\s*(?:tasks|todos|to-dos|to dos|items)",
                r"(?:pending|incomplete|open|remaining)\s+(?:tasks|todos|to-dos|to dos|items)",
                r"(?:completed|done|finished|closed)\s+(?:tasks|todos|to-dos|to dos|items)",
                r"(?:what's|what is)\s+(?:on|in)\s+(?:my\s+)?(?:list|todo|to-do|tasks)",
            ],
            "complete_task": [
                r"(?:complete|finish|done|mark as done|check off|tick off)\s+(?:task|item)?\s*(?:number|#)?\s*(\d+)",
                r"(?:mark|set|make)\s+(?:task|item)?\s*(?:number|#)?\s*(\d+)\s+(?:as\s+)?(?:complete|finished|done)",
                r"(?:complete|finish|done)\s+(?:the\s+)?(.+?)\s+(?:task|item)",
                r"(\d+)\s+(?:is\s+)?(?:complete|done|finished)",
            ],
            "update_task": [
                r"(?:update|change|modify|edit|rename)\s+(?:task|item)?\s*(?:number|#)?\s*(\d+)\s+(?:to|as|with)\s+(.+)",
                r"(?:change|update|modify|edit)\s+(?:the\s+)?(.+?)\s+(?:task|item)\s+(?:to|as|with)\s+(.+)",
                r"(?:update|change|modify|edit)\s+(?:task|item)?\s*(?:number|#)?\s*(\d+)\s+(?:title|name|description)\s+(?:to|as)\s+(.+)",
            ],
            "delete_task": [
                r"(?:delete|remove|eliminate|get rid of|trash|discard)\s+(?:task|item)?\s*(?:number|#)?\s*(\d+)",
                r"(?:delete|remove|eliminate|get rid of|trash|discard)\s+(?:the\s+)?(.+?)\s+(?:task|item)",
                r"(?:remove|delete)\s+(?:task|item)?\s*(?:number|#)?\s*(\d+)\s+(?:from|off)\s+(?:my\s+)?(?:list|tasks|todos)",
            ]
        }

    def detect_intent(self, text: str, context_messages: list = None) -> Dict[str, Any]:
        """
        Detect the intent from the given text, considering conversation context if available.

        Args:
            text: The user's input text
            context_messages: Optional list of previous messages for context

        Returns:
            Dictionary containing the detected operation and parameters
        """
        text_lower = text.lower().strip()

        # Check if this is a confirmation for a destructive operation (like "yes", "confirm", etc.)
        # when the previous message was asking for confirmation
        if context_messages:
            # Look at the last message to see if it was asking for confirmation
            last_message = context_messages[-1] if context_messages else None
            if last_message and "confirm" in last_message.get("content", "").lower():
                confirmation_keywords = ["yes", "confirm", "ok", "okay", "sure", "delete", "go ahead", "proceed", "affirmative"]

                if any(keyword in text_lower for keyword in confirmation_keywords):
                    # Return a special confirmation intent
                    return {
                        "operation": "confirm_destructive_action",
                        "params": {}
                    }

        # Check each intent pattern
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    groups = match.groups()

                    if intent == "add_task":
                        # Extract the task description
                        task_description = groups[0].strip() if groups else text
                        # Remove common prefixes like "to buy", "that i need to", etc.
                        task_description = re.sub(r'^(?:to|that i need to|that i have to|to go and|just)\s+', '', task_description)
                        return {
                            "operation": "add_task",
                            "params": {
                                "title": task_description[:50],  # Limit title length
                                "description": task_description
                            }
                        }
                    elif intent in ["list_tasks"]:
                        # Check for specific status
                        if "pending" in text_lower or "incomplete" in text_lower or "open" in text_lower or "remaining" in text_lower:
                            status = "pending"
                        elif "completed" in text_lower or "done" in text_lower or "finished" in text_lower or "closed" in text_lower:
                            status = "completed"
                        else:
                            status = None

                        return {
                            "operation": intent,
                            "params": {
                                "status": status
                            }
                        }
                    elif intent in ["complete_task", "delete_task"]:
                        # Extract task ID
                        task_id_str = groups[0] if groups else None
                        if task_id_str and task_id_str.isdigit():
                            return {
                                "operation": intent,
                                "params": {
                                    "task_id": int(task_id_str)
                                }
                            }
                    elif intent == "update_task":
                        # Extract task ID and new content
                        if len(groups) >= 2:
                            # If we have task_id and new content
                            task_id_str = groups[0]
                            if task_id_str.isdigit():
                                new_content = groups[1]
                                return {
                                    "operation": intent,
                                    "params": {
                                        "task_id": int(task_id_str),
                                        "title": new_content[:50],
                                        "description": new_content
                                    }
                                }

                        # Alternative: if we have task description and new content
                        elif len(groups) >= 2:
                            # This would require looking up the task by description
                            # For now, we'll return a more generic response
                            pass

        # If no pattern matches, return unknown intent
        return {
            "operation": "unknown",
            "params": {}
        }

    def extract_task_params(self, text: str) -> Dict[str, str]:
        """
        Helper method to extract task parameters from text.

        Args:
            text: The text to extract parameters from

        Returns:
            Dictionary containing extracted parameters
        """
        # This is a helper method that could be used to extract more detailed parameters
        # from user input, such as due dates, priorities, etc.
        return {}