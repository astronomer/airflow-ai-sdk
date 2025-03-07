"""
Module that contains the AgentOperator class.
"""

from typing import Any

from pydantic import BaseModel
from pydantic_ai import Agent, models

from airflow_ai_sdk.operators.agent import AgentDecoratedOperator


class LLMDecoratedOperator(AgentDecoratedOperator):
    """
    Provides an abstraction on top of the Agent class. Not as powerful as the Agent class, but
    provides a simpler interface.
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
