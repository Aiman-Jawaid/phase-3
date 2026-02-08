from typing import Dict, Any, List
from .cohere_client import CohereClientWrapper
from ..mcp_tools.add_task import add_task
from ..mcp_tools.list_tasks import list_tasks
from ..mcp_tools.update_task import update_task
from ..mcp_tools.complete_task import complete_task
from ..mcp_tools.delete_task import delete_task
from ..agents.tool_registry import ToolRegistry


class TaskOrchestrationService:
    """
    Service that orchestrates task operations based on natural language input
    and coordinates with the agent and MCP tools.
    """

    def __init__(self, cohere_client: CohereClientWrapper):
        self.cohere_client = cohere_client
        self.tool_registry = ToolRegistry()

        # Register all MCP tools
        self.tool_registry.register_tool("add_task", add_task)
        self.tool_registry.register_tool("list_tasks", list_tasks)
        self.tool_registry.register_tool("update_task", update_task)
        self.tool_registry.register_tool("complete_task", complete_task)
        self.tool_registry.register_tool("delete_task", delete_task)

    def execute_task_operation(self, user_id: str, operation: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a specific task operation based on the operation type.

        Args:
            user_id: The ID of the authenticated user
            operation: The operation to perform (add_task, list_tasks, etc.)
            **kwargs: Operation-specific arguments

        Returns:
            Result of the operation
        """
        if operation == "add_task":
            return add_task(user_id, kwargs.get("title"), kwargs.get("description"))
        elif operation == "list_tasks":
            return list_tasks(user_id, kwargs.get("status"))
        elif operation == "update_task":
            return update_task(
                user_id,
                kwargs["task_id"],
                title=kwargs.get("title"),
                description=kwargs.get("description"),
                completed=kwargs.get("completed")
            )
        elif operation == "complete_task":
            return complete_task(user_id, kwargs["task_id"], kwargs.get("completed", True))
        elif operation == "delete_task":
            confirmed = kwargs.get("confirmed", False)
            task_id = kwargs.get("task_id")

            return delete_task(user_id, task_id, confirmed=confirmed)
        else:
            # For unknown operations, return a message indicating the operation is not recognized
            # This prevents errors when the intent detector picks up something that's not a task operation
            return {
                "success": True,
                "message": "I'm not sure how to handle that request. I can help you with tasks like adding, listing, completing, updating, or deleting tasks. For example, you can say 'Add a task to buy groceries' or 'Show my tasks'."
            }

    def get_available_tools(self) -> List[str]:
        """
        Get list of available tools.

        Returns:
            List of available tool names
        """
        return self.tool_registry.get_tool_names()