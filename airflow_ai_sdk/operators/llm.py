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

    def __init__(
        self,
        model: models.Model | models.KnownModelName,
        system_prompt: str,
        result_type: type[BaseModel] = str,
        output_type: type[BaseModel] | None = None,
        **kwargs: dict[str, Any],
    ):
        """
        Initialize the LLMDecoratedOperator.

        Args:
            model: The LLM model to use for the call.
            system_prompt: The system prompt to use for the call.
            result_type: (Deprecated) Optional Pydantic model type to validate and parse the result.
                        Use output_type instead.
            output_type: Optional Pydantic model type to validate and parse the result.
            **kwargs: Additional keyword arguments for the operator.
        """
        # Handle parameter deprecation - prioritize output_type if provided
        if output_type is not None:
            # If both are provided, output_type takes precedence and we warn about result_type
            if result_type != str:  # str is the default, so only warn if explicitly set
                warnings.warn(
                    "`result_type` is deprecated, use `output_type` instead.", 
                    DeprecationWarning, 
                    stacklevel=2
                )
            final_output_type = output_type
        else:
            # Use result_type as fallback, warn if it's not the default
            if result_type != str:
                warnings.warn(
                    "`result_type` is deprecated, use `output_type` instead.", 
                    DeprecationWarning, 
                    stacklevel=2
                )
            final_output_type = result_type
        
        agent = Agent(
            model=model,
            system_prompt=system_prompt,
            output_type=final_output_type,
        )
        super().__init__(agent=agent, **kwargs)
