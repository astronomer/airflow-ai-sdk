"""
Module that contains the AirflowTool class.
"""

from pydantic_ai import Tool as PydanticTool
from pydantic_ai.tools import AgentDepsT, RunContext, _messages


class WrappedTool(PydanticTool[AgentDepsT]):
    """
    Wrapper around the pydantic_ai.Tool class that prints the tool call and the result
    in an airflow log group for better observability.
    """

    async def run(
        self, message: _messages.ToolCallPart, run_context: RunContext[AgentDepsT]
    ) -> _messages.ToolReturnPart | _messages.RetryPromptPart:
        from pprint import pprint

        print(f"::group::Calling tool {message.tool_name} with args {message.args}")

        result = await super().run(message, run_context)
        print("Result")
        pprint(result.content)

        print(f"::endgroup::")

        return result

    @classmethod
    def from_pydantic_tool(
        cls, tool: PydanticTool[AgentDepsT]
    ) -> "WrappedTool[AgentDepsT]":
        return cls(
            tool.function,
            name=tool.name,
            description=tool.description,
        )
