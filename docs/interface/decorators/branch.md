# airflow_ai_sdk.decorators.branch

This module contains the decorators for the llm_branch decorator.

## llm_branch

Decorator to branch a DAG based on the result of an LLM call.

Example:

```python
@task.llm_branch(model="o3-mini", system_prompt="Return 'a' or 'b'")
def decide() -> str:
    return "Which path?"
```
