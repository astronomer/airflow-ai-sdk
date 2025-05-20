# airflow_ai_sdk.decorators.agent

This module contains the decorators for the agent.

## agent

Decorator to execute an :class:`pydantic_ai.Agent` inside an Airflow task.

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

