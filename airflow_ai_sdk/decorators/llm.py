"""
This module contains the decorators for the llm decorator.
"""

from typing import TYPE_CHECKING, Any

from airflow.decorators.base import task_decorator_factory
from pydantic_ai import models

from airflow_ai_sdk.models.base import BaseModel
from airflow_ai_sdk.operators.llm import LLMDecoratedOperator

if TYPE_CHECKING:
    from airflow.decorators.base import TaskDecorator


def llm(
    model: models.Model | models.KnownModelName,
    system_prompt: str,
    result_type: type[BaseModel] | None = None,
    **kwargs: dict[str, Any],
) -> "TaskDecorator":
    """
    Decorator to make LLM calls.
    """
    kwargs["model"] = model
    kwargs["result_type"] = result_type
    kwargs["system_prompt"] = system_prompt
    return task_decorator_factory(
        decorated_operator_class=LLMDecoratedOperator,
        **kwargs,
    )
