# airflow_ai_sdk.operators.agent

This module provides the AgentDecoratedOperator class for executing pydantic_ai.Agent
instances within Airflow tasks.

## AgentDecoratedOperator

Operator that executes a `pydantic_ai.Agent`.

This operator wraps a `pydantic_ai.Agent` instance and executes it within an Airflow task.
It provides enhanced logging capabilities through `WrappedTool`.

Example:

```python
from pydantic_ai import Agent
from airflow_ai_sdk.operators.agent import AgentDecoratedOperator

def prompt() -> str:
    return "Hello"

operator = AgentDecoratedOperator(
    task_id="example",
    python_callable=prompt,
    agent=Agent(model="o3-mini", system_prompt="Say hello"),
)
```
