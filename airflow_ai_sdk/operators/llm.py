"""
Module that contains the AgentOperator class.
"""

from typing import Any

from pydantic import BaseModel
from pydantic_ai import Agent, models

from airflow_ai_sdk.operators.agent import AgentDecoratedOperator


class LLMDecoratedOperator(AgentDecoratedOperator):
    """Simpler interface for performing a single LLM call.

    Example:
        ```python
        from airflow_ai_sdk.operators.llm import LLMDecoratedOperator

        def make_prompt() -> str:
            return "Hello"

        operator = LLMDecoratedOperator(
            task_id="llm",
            python_callable=make_prompt,
            model="o3-mini",
            system_prompt="Reply politely",
        )
        ```
    """

    custom_operator_name = "@task.llm"

    def __init__(
        self,
        model: models.Model | models.KnownModelName,
        system_prompt: str,
        result_type: type[BaseModel] = str,
        **kwargs: dict[str, Any],
    ):
        agent = Agent(
            model=model,
            system_prompt=system_prompt,
            result_type=result_type,
        )

        super().__init__(agent=agent, **kwargs)
