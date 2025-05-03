"""
This module contains the decorators for embedding.
"""

from typing import TYPE_CHECKING, Any

from airflow_ai_sdk.airflow import task_decorator_factory
from airflow_ai_sdk.operators.embed import EmbedDecoratedOperator

if TYPE_CHECKING:
    from airflow_ai_sdk.airflow import TaskDecorator


def embed(text: str, model: str, **kwargs: dict[str, Any]) -> "TaskDecorator":
    """
    Decorator to make agent calls.
    """
    kwargs["text"] = text
    kwargs["model"] = model
    return task_decorator_factory(
        decorated_operator_class=EmbedDecoratedOperator,
        **kwargs,
    )
