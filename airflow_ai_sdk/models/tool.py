"""
This module provides a wrapper around pydantic_ai.Tool for better observability in Airflow.
"""

from pydantic_ai import Tool as PydanticTool
from pydantic_ai.messages import RetryPromptPart, ToolCallPart, ToolReturnPart
from pydantic_ai.tools import AgentDepsT


class WrappedTool(PydanticTool[AgentDepsT]):
    """
    Wrapper around `pydantic_ai.Tool` for better observability in Airflow.

    This class extends the `pydantic_ai.Tool` class to provide enhanced logging
    capabilities in Airflow. It wraps tool calls and results in log groups for
    better visibility in the Airflow UI.

    Example:

    ```python
    from airflow_ai_sdk.models.tool import WrappedTool
    from pydantic_ai import Tool

    tool = Tool(my_function, name="my_tool")
    wrapped_tool = WrappedTool.from_pydantic_tool(tool)
    ```
    """

    async def run(
        self,
        message: ToolCallPart,
        *args: object,
        **kwargs: object,
    ) -> ToolReturnPart | RetryPromptPart:
        """
        Execute the tool with enhanced logging.

        Args:
            message: The tool call message containing the tool name and arguments.
            *args: Additional positional arguments for the tool.
            **kwargs: Additional keyword arguments for the tool.

        Returns:
            The tool's return value wrapped in a ToolReturnPart or RetryPromptPart.
        """
        from pprint import pprint

        print(f"::group::Calling tool {message.tool_name} with args {message.args}")

        result = await super().run(message, *args, **kwargs)
        print("Result")
        pprint(result.content)

        print(f"::endgroup::")

        return result

    @classmethod
    def from_pydantic_tool(
        cls, tool: PydanticTool[AgentDepsT]
    ) -> "WrappedTool[AgentDepsT]":
        """
        Create a WrappedTool instance from a pydantic_ai.Tool.

        Args:
            tool: The pydantic_ai.Tool instance to wrap.

        Returns:
            A new WrappedTool instance with the same configuration as the input tool.
        """
        return cls(
            tool.function,
            name=tool.name,
            description=tool.description,
        )
