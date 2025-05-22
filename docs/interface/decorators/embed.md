# airflow_ai_sdk.decorators.embed

This module contains the decorators for embedding.

## embed

Decorator to embed text using a SentenceTransformer model.

Args:
    model_name: The name of the model to use for the embedding. Passed to
        the `SentenceTransformer` constructor.
    **kwargs: Keyword arguments to pass to the `EmbedDecoratedOperator`
        constructor.

Example:

```python
@task.embed()
def vectorize() -> str:
    return "Example text"
```
