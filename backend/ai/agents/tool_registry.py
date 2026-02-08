from typing import Dict, Callable, Any
from functools import wraps


class ToolRegistry:
    """
    Registry for managing MCP tools that the agent can call.
    """

    def __init__(self):
        self.tools: Dict[str, Callable] = {}

    def register_tool(self, name: str, func: Callable) -> None:
        """
        Register a tool with the registry.

        Args:
            name: The name of the tool
            func: The function that implements the tool
        """
        self.tools[name] = func

    def get_tool(self, name: str) -> Callable:
        """
        Get a registered tool by name.

        Args:
            name: The name of the tool

        Returns:
            The tool function
        """
        if name not in self.tools:
            raise KeyError(f"Tool '{name}' is not registered")
        return self.tools[name]

    def execute_tool(self, name: str, *args, **kwargs) -> Any:
        """
        Execute a registered tool with the given arguments.

        Args:
            name: The name of the tool to execute
            *args: Positional arguments to pass to the tool
            **kwargs: Keyword arguments to pass to the tool

        Returns:
            The result of the tool execution
        """
        tool = self.get_tool(name)
        return tool(*args, **kwargs)

    def get_tool_names(self) -> list:
        """
        Get a list of all registered tool names.

        Returns:
            List of tool names
        """
        return list(self.tools.keys())

    def list_tools(self) -> Dict[str, str]:
        """
        Get a dictionary of tool names and their descriptions.

        Returns:
            Dictionary mapping tool names to descriptions
        """
        # For now, we'll just return the names without descriptions
        # In a more sophisticated implementation, we'd store and return descriptions
        return {name: f"Tool: {name}" for name in self.tools.keys()}