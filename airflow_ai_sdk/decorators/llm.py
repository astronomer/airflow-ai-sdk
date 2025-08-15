"""
This module contains the decorators for the llm decorator.
"""

import warnings
from typing import TYPE_CHECKING, Any

from pydantic_ai import models

from airflow_ai_sdk.airflow import task_decorator_factory
from airflow_ai_sdk.models.base import BaseModel
from airflow_ai_sdk.operators.llm import LLMDecoratedOperator

if TYPE_CHECKING:
    from airflow_ai_sdk.airflow import TaskDecorator


def llm(
    model: models.Model | models.KnownModelName,
    system_prompt: str,
    result_type: type[BaseModel] | None = None,
    output_type: type[BaseModel] | None = None,
    **kwargs: dict[str, Any],
) -> "TaskDecorator":
    """
    Decorator to make a single call to an LLM.

    Args:
        model: The LLM model to use for the call.
        system_prompt: The system prompt to use for the call.
        result_type: (Deprecated) Optional Pydantic model type to validate and parse the result.
                    Use output_type instead.
        output_type: Optional Pydantic model type to validate and parse the result.
        **kwargs: Additional keyword arguments for the operator.

    Example:

    ```python
    @task.llm(model="o3-mini", system_prompt="Translate to French")
    def translate(text: str) -> str:
        return text
    ```
    """
    # Handle parameter deprecation
    if result_type is not None and output_type is not None:
        raise TypeError("`result_type` and `output_type` cannot be set at the same time.")
    
    if result_type is not None:
        warnings.warn(
            "`result_type` is deprecated, use `output_type` instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        output_type = result_type
    
    kwargs["model"] = model
    kwargs["output_type"] = output_type
    kwargs["system_prompt"] = system_prompt
    return task_decorator_factory(
        decorated_operator_class=LLMDecoratedOperator,
        **kwargs,
    )
