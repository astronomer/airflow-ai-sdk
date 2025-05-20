# airflow_ai_sdk.operators.embed

Module that contains the EmbedOperator class.

## EmbedDecoratedOperator

Operator that builds embeddings for text.

Example:
    ```python
    from airflow_ai_sdk.operators.embed import EmbedDecoratedOperator

    def produce_text() -> str:
        return "document"

    operator = EmbedDecoratedOperator(
        task_id="embed",
        python_callable=produce_text,
        op_args=[],
        op_kwargs={},
        model_name="all-MiniLM-L12-v2",
    )
    ```

