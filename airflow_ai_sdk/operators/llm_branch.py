"""
This module provides the LLMBranchDecoratedOperator class for branching DAGs based on
LLM decisions within Airflow tasks.
"""

from enum import Enum
from typing import Any

from pydantic_ai import Agent, models

from airflow_ai_sdk.airflow import BranchMixIn, Context
from airflow_ai_sdk.operators.agent import AgentDecoratedOperator


class LLMBranchDecoratedOperator(AgentDecoratedOperator, BranchMixIn):
    """
    Branch a DAG based on the result of an LLM call.

    This operator uses an LLM to decide which downstream task to execute next.
    It combines the capabilities of an LLM with Airflow's branching functionality.

    Example:

    ```python
    from airflow_ai_sdk.operators.llm_branch import LLMBranchDecoratedOperator

    def make_prompt() -> str:
        return "Choose"

    operator = LLMBranchDecoratedOperator(
        task_id="branch",
        python_callable=make_prompt,
        model="o3-mini",
        system_prompt="Return 'a' or 'b'",
    )
    ```
    """

    custom_operator_name = "@task.llm_branch"

    def __init__(
        self,
        model: models.Model | models.KnownModelName,
        system_prompt: str,
        allow_multiple_branches: bool = False,
        **kwargs: dict[str, Any],
    ):
        """
        Initialize the LLMBranchDecoratedOperator.

        Args:
            model: The LLM model to use for the decision.
            system_prompt: The system prompt to use for the decision.
            allow_multiple_branches: Whether to allow multiple downstream tasks to be executed.
            **kwargs: Additional keyword arguments for the operator.
        """
        self.model = model
        self.system_prompt = system_prompt
        self.allow_multiple_branches = allow_multiple_branches

        agent = Agent(
            model=model,
            system_prompt=system_prompt,
        )

        super().__init__(agent=agent, **kwargs)

    def execute(self, context: Context) -> str | list[str]:
        """
        Execute the branching decision with the given context.

        Args:
            context: The Airflow context for this task execution.

        Returns:
            The task_id(s) of the downstream task(s) to execute next.
        """
        # create an enum of the downstream tasks and add it to the agent
        downstream_tasks_enum = Enum(
            "DownstreamTasks",
            {task_id: task_id for task_id in self.downstream_task_ids},
        )

        self.agent = Agent(
            model=self.model,
            system_prompt=self.system_prompt,
            result_type=downstream_tasks_enum,
        )

        result = super().execute(context)

        # turn the result into a string
        if isinstance(result, Enum):
            result = result.value

        # if the response is not a string, cast it to a string
        if not isinstance(result, str):
            result = str(result)

        if isinstance(result, list) and not self.allow_multiple_branches:
            raise ValueError(
                "Multiple branches were returned but allow_multiple_branches is False"
            )

        return self.do_branch(context, result)
