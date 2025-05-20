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
    """Decorator to branch a DAG based on the result of an LLM call.

    Example:
        >>> import airflow_ai_sdk as ai_sdk
        >>> @ai_sdk.llm_branch(model="o3-mini", system_prompt="Return 'a' or 'b'")
        ... def decide() -> str:
        ...     return "Which path?"
    """
    kwargs["model"] = model
    kwargs["system_prompt"] = system_prompt
    kwargs["allow_multiple_branches"] = allow_multiple_branches
    return task_decorator_factory(
        decorated_operator_class=LLMBranchDecoratedOperator,
        **kwargs,
    )
