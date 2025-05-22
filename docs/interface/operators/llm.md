# airflow_ai_sdk.operators.llm

This module provides the LLMDecoratedOperator class for making single LLM calls
within Airflow tasks.

## LLMDecoratedOperator

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
