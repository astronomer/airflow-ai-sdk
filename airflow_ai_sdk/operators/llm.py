"""
This module provides the LLMDecoratedOperator class for making single LLM calls
within Airflow tasks.
"""

from typing import Any

from pydantic import BaseModel
from pydantic_ai import Agent, models

from airflow_ai_sdk.airflow import Context
from airflow_ai_sdk.operators.agent import AgentDecoratedOperator


class LLMDecoratedOperator(AgentDecoratedOperator):
    """
    Simpler interface for performing a single LLM call.

    This operator provides a simplified interface for making single LLM calls within
    Airflow tasks, without the full agent functionality.

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
        """
        Initialize the LLMDecoratedOperator.

        Args:
            model: The LLM model to use for the call.
            system_prompt: The system prompt to use for the call.
            result_type: Optional Pydantic model type to validate and parse the result.
            **kwargs: Additional keyword arguments for the operator.
        """
        agent = Agent(
            model=model,
            system_prompt=system_prompt,
            result_type=result_type,
        )
        super().__init__(agent=agent, **kwargs)
