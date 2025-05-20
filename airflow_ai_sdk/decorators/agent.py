"""
This module contains the decorators for the agent.
"""

from typing import TYPE_CHECKING, Any

from pydantic_ai.agent import Agent

from airflow_ai_sdk.airflow import task_decorator_factory
from airflow_ai_sdk.operators.agent import AgentDecoratedOperator

if TYPE_CHECKING:
    from airflow_ai_sdk.airflow import TaskDecorator


def agent(agent: Agent, **kwargs: dict[str, Any]) -> "TaskDecorator":
    """Decorator to execute an :class:`pydantic_ai.Agent` inside an Airflow task.

    Example:
        ```python
        from airflow.decorators import task
        from pydantic_ai import Agent
        import airflow_ai_sdk as ai_sdk

        my_agent = Agent(model="o3-mini", system_prompt="Say hello")

        @task
        @ai_sdk.agent(my_agent)
        def greet(name: str) -> str:
            return name
        ```
    """
    kwargs["agent"] = agent
    return task_decorator_factory(
        decorated_operator_class=AgentDecoratedOperator,
        **kwargs,
    )
