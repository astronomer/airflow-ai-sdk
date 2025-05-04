"""
This module contains the decorators for embedding.
"""

from typing import TYPE_CHECKING, Any

from airflow_ai_sdk.airflow import task_decorator_factory
from airflow_ai_sdk.operators.embed import EmbedDecoratedOperator

if TYPE_CHECKING:
    from airflow_ai_sdk.airflow import TaskDecorator


def embed(
    model_name: str = "all-MiniLM-L12-v2", **kwargs: dict[str, Any]
) -> "TaskDecorator":
    """
    Decorator to make embed some text.
    """
    # kwargs["text"] = text
    kwargs["model_name"] = model_name
    return task_decorator_factory(
        decorated_operator_class=EmbedDecoratedOperator,
        **kwargs,
    )
