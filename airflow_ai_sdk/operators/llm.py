"""
This module provides the LLMDecoratedOperator class for making single LLM calls
within Airflow tasks.
"""

import warnings
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

    # Used for distinguishing user-provided values vs default value
    _sentinel = object()

    def __init__(
        self,
        model: models.Model | models.KnownModelName,
        system_prompt: str,
        # TODO change to type[BaseModel] = str in 1.0.0
        output_type: type[BaseModel] | None = _sentinel,
        # Deprecated. Will be removed in 1.0.0
        result_type: type[BaseModel] | None = _sentinel,
        **kwargs: dict[str, Any],
    ):
        """
        Initialize the LLMDecoratedOperator.

        Args:
            model: The LLM model to use for the call.
            system_prompt: The system prompt to use for the call.
            output_type: Optional Pydantic model type to validate and parse the result.
            **kwargs: Additional keyword arguments for the operator.
        """

        # In pydantic-ai==0.6.0, result_type was replaced by output_type. In airflow-ai-sdk, to avoid breaking
        # changes, we'd like to support result_type until airflow-ai-sdk==1.0.0.
        # Because we want to raise a DeprecationWarning in case the user configures result_type, the arguments
        # default to a sentinel value, which enables us to distinguish between user-supplied values and
        # default values. This can be removed once we release airflow-ai-sdk==1.0.0.
        if output_type is self._sentinel and result_type is self._sentinel:
            # User didn't configure either, default to str
            output_type = str
        elif output_type is not self._sentinel and result_type is self._sentinel:
            # User configured output_type, leave as-is
            pass
        elif output_type is self._sentinel and result_type is not self._sentinel:
            # User configured result_type, raise DeprecationWarning and map to output_type
            warnings.warn(
                "Argument `result_type` is deprecated and will be removed in version 1.0.0. "
                "Use `output_type` instead.",
                category=DeprecationWarning,
                stacklevel=2,  # Points to the user code
            )
            output_type = result_type
        else:
            # User configured both output_type and result_type, raise error
            raise ValueError(
                "Provide only one of `output_type` (preferred) or `result_type` (deprecated), not both."
            )

        agent = Agent(
            model=model,
            system_prompt=system_prompt,
            output_type=output_type,
        )
        super().__init__(agent=agent, **kwargs)
