# airflow_ai_sdk.decorators.agent

This module contains the decorators for the agent.

## agent

Decorator to execute an `pydantic_ai.Agent` inside an Airflow task.

Example:

```python
from pydantic_ai import Agent

my_agent = Agent(model="o3-mini", system_prompt="Say hello")

@task.agent(my_agent)
def greet(name: str) -> str:
    return name
```
