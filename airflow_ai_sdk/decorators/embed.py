"""
This module contains the decorators for embedding.
"""

from typing import TYPE_CHECKING, Any

from airflow_ai_sdk.airflow import task_decorator_factory
from airflow_ai_sdk.operators.embed import EmbedDecoratedOperator

if TYPE_CHECKING:
    from airflow_ai_sdk.airflow import TaskDecorator


def embed(
    model_name: str = "all-MiniLM-L12-v2",
    **kwargs: dict[str, Any],
) -> "TaskDecorator":
    """
    Decorator to embed text using a SentenceTransformer model.

    Args:
        model_name: The name of the model to use for the embedding. Passed to
            the `SentenceTransformer` constructor.
        **kwargs: Keyword arguments to pass to the `EmbedDecoratedOperator`
            constructor.

    Example:

    ```python
    @task.embed()
    def vectorize() -> str:
        return "Example text"
    ```
    """
    kwargs["model_name"] = model_name
    return task_decorator_factory(
        decorated_operator_class=EmbedDecoratedOperator,
        **kwargs,
    )
