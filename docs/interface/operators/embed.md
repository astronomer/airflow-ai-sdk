# airflow_ai_sdk.operators.embed

This module provides the EmbedDecoratedOperator class for generating text embeddings
using SentenceTransformer models within Airflow tasks.

## EmbedDecoratedOperator

Operator that builds embeddings for text using SentenceTransformer models.

This operator generates embeddings for text input using a specified SentenceTransformer
model. It provides a convenient way to create embeddings within Airflow tasks.

Example:

```python
from airflow_ai_sdk.operators.embed import EmbedDecoratedOperator

def produce_text() -> str:
    return "document"

operator = EmbedDecoratedOperator(
    task_id="embed",
    python_callable=produce_text,
    model_name="all-MiniLM-L12-v2",
)
```
