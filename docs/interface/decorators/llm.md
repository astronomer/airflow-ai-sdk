# airflow_ai_sdk.decorators.llm

This module contains the decorators for the llm decorator.

## llm

Decorator to make a single call to an LLM.

Example:

```python
@task.llm(model="o3-mini", system_prompt="Translate to French")
def translate(text: str) -> str:
    return text
```
