"""
Module that contains the AgentOperator class.
"""

from enum import Enum
from typing import Any

from airflow.operators.branch import BranchMixIn
from airflow.utils.context import Context
from pydantic_ai import Agent, models

from airflow_ai_sdk.operators.agent import AgentDecoratedOperator


class LLMBranchDecoratedOperator(AgentDecoratedOperator, BranchMixIn):
    """
    A decorator that branches the execution of a DAG based on the result of an LLM call.
    """

    custom_operator_name = "@task.llm_branch"

    def __init__(
        self,
        model: models.Model | models.KnownModelName,
        system_prompt: str,
        allow_multiple_branches: bool = False,
        **kwargs: dict[str, Any],
    ):
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
        Picks a downstream task based on the result of an LLM call.
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

        # execute the agent
        response = super().execute(context)

        # turn the result into a string
        if isinstance(response, Enum):
            response = response.value

        # if the response is not a string, cast it to a string
        if not isinstance(response, str):
            response = str(response)

        return self.do_branch(context, response)
