# airflow_ai_sdk.decorators.branch

This module contains the decorators for the llm_branch decorator.

## llm_branch

Decorator to branch a DAG based on the result of an LLM call.

Example:

```python
@task
def handle_positive_sentiment(text: str) -> str:
    return "Handle positive sentiment"

@task
def handle_negative_sentiment(text: str) -> str:
    return "Handle negative sentiment"

@task.llm_branch(model="o3-mini", system_prompt="Classify this text by sentiment")
def decide(text: str) -> str:
    return text

# then, in the DAG:
decide >> [handle_positive_sentiment, handle_negative_sentiment]
```
