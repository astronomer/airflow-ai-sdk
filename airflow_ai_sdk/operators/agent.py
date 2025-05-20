"""
Module that contains the AgentOperator class.
"""

from typing import Any

from pydantic_ai import Agent

from airflow_ai_sdk.airflow import Context, _PythonDecoratedOperator
from airflow_ai_sdk.models.base import BaseModel
from airflow_ai_sdk.models.tool import WrappedTool


class AgentDecoratedOperator(_PythonDecoratedOperator):
    """Operator that executes a :class:`pydantic_ai.Agent`.

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
            op_args=[],
            op_kwargs={},
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
        super().__init__(*args, op_args=op_args, op_kwargs=op_kwargs, **kwargs)

        self.op_args = op_args
        self.op_kwargs = op_kwargs
        self.agent = agent

        # wrapping the tool will print the tool call and the result in an airflow log group for better observability
        self.agent._function_tools = {
            name: WrappedTool.from_pydantic_tool(tool)
            for name, tool in self.agent._function_tools.items()
        }

    def execute(self, context: Context) -> str | dict[str, Any] | list[str]:
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
        if isinstance(result.data, BaseModel):
            return result.data.model_dump()

        return result.data
