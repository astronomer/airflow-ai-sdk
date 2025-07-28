"""
This module provides the AgentDecoratedOperator class for executing pydantic_ai.Agent
instances within Airflow tasks.
"""

from typing import Any

from pydantic_ai import Agent

from airflow_ai_sdk.airflow import Context, _PythonDecoratedOperator
from airflow_ai_sdk.models.base import BaseModel
from airflow_ai_sdk.models.tool import WrappedTool


class AgentDecoratedOperator(_PythonDecoratedOperator):
    """
    Operator that executes a `pydantic_ai.Agent`.

    This operator wraps a `pydantic_ai.Agent` instance and executes it within an Airflow task.
    It provides enhanced logging capabilities through `WrappedTool`.

    Example:

    ```python
    from pydantic_ai import Agent
    from airflow_ai_sdk.operators.agent import AgentDecoratedOperator

    def prompt() -> str:
        return "Hello"

    operator = AgentDecoratedOperator(
        task_id="example",
        python_callable=prompt,
        agent=Agent(model="o3-mini", system_prompt="Say hello"),
    )
    ```
    """

    custom_operator_name = "@task.agent"

    def __init__(
        self,
        agent: Agent,
        op_args: list[Any],
        op_kwargs: dict[str, Any],
        *args: dict[str, Any],
        **kwargs: dict[str, Any],
    ):
        """
        Initialize the AgentDecoratedOperator.

        Args:
            agent: The `pydantic_ai.Agent` instance to execute.
            op_args: Positional arguments to pass to the `python_callable`.
            op_kwargs: Keyword arguments to pass to the `python_callable`.
            *args: Additional positional arguments for the operator.
            **kwargs: Additional keyword arguments for the operator.
        """
        super().__init__(*args, op_args=op_args, op_kwargs=op_kwargs, **kwargs)

        self.op_args = op_args
        self.op_kwargs = op_kwargs
        self.agent = agent

        # wrapping the tool will print the tool call and the result in an airflow log group for better observability
        if (
            hasattr(self.agent, "_function_toolset")
            and self.agent._function_toolset.tools
        ):
            wrapped_tools = {
                name: WrappedTool.from_pydantic_tool(tool)
                for name, tool in self.agent._function_toolset.tools.items()
            }
            # Replace the tools in the toolset with wrapped versions
            self.agent._function_toolset.tools = wrapped_tools

    def execute(self, context: Context) -> str | dict[str, Any] | list[str]:
        """
        Execute the agent with the given context.

        Args:
            context: The Airflow context for this task execution.

        Returns:
            The result of the agent's execution, which can be a string, dictionary,
            or list of strings.
        """
        print("Executing LLM call")

        prompt = super().execute(context)
        print(f"Prompt: {prompt}")

        try:
            result = self.agent.run_sync(prompt)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
            raise e

        # turn the result into a dict
        if isinstance(result.output, BaseModel):
            return result.output.model_dump()

        return result.output
