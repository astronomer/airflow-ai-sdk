"""
This module contains the decorators for the llm_branch decorator.
"""

from typing import TYPE_CHECKING, Any

from airflow.decorators.base import task_decorator_factory
from pydantic_ai import models

from airflow_ai_sdk.operators.llm_branch import LLMBranchDecoratedOperator

if TYPE_CHECKING:
    from airflow.decorators.base import TaskDecorator


def llm_branch(
    model: models.Model | models.KnownModelName,
    system_prompt: str,
    allow_multiple_branches: bool = False,
    **kwargs: dict[str, Any],
) -> "TaskDecorator":
    """
    Decorator to make LLM calls and branch the execution of a DAG based on the result.
    """
    kwargs["model"] = model
    kwargs["system_prompt"] = system_prompt
    kwargs["allow_multiple_branches"] = allow_multiple_branches
    return task_decorator_factory(
        decorated_operator_class=LLMBranchDecoratedOperator,
        **kwargs,
    )
