"""
This module contains the decorators for the llm_branch decorator.
"""

from typing import TYPE_CHECKING, Any

from pydantic_ai import models

from airflow_ai_sdk.airflow import task_decorator_factory
from airflow_ai_sdk.operators.llm_branch import LLMBranchDecoratedOperator

if TYPE_CHECKING:
    from airflow_ai_sdk.airflow import TaskDecorator


def llm_branch(
    model: models.Model | models.KnownModelName,
    system_prompt: str,
    allow_multiple_branches: bool = False,
    **kwargs: dict[str, Any],
) -> "TaskDecorator":
    """
    Decorator to branch a DAG based on the result of an LLM call.

    Example:

    ```python
    @task
    def handle_positive_sentiment(text: str) -> str:
        return "Handle positive sentiment"

    @task
    def handle_negative_sentiment(text: str) -> str:
        return "Handle negative sentiment"

    @task.llm_branch(model="o3-mini", system_prompt="Classify this text by sentiment")
    def decide(text: str) -> str:
        return text

    # then, in the DAG:
    decide >> [handle_positive_sentiment, handle_negative_sentiment]
    ```
    """
    kwargs["model"] = model
    kwargs["system_prompt"] = system_prompt
    kwargs["allow_multiple_branches"] = allow_multiple_branches
    return task_decorator_factory(
        decorated_operator_class=LLMBranchDecoratedOperator,
        **kwargs,
    )
