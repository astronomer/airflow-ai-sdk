"""
This module provides the EmbedDecoratedOperator class for generating text embeddings
using SentenceTransformer models within Airflow tasks.
"""

from typing import Any

from airflow_ai_sdk.airflow import Context, _PythonDecoratedOperator


class EmbedDecoratedOperator(_PythonDecoratedOperator):
    """
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
    """

    custom_operator_name = "@task.embed"

    def __init__(
        self,
        op_args: list[Any],
        op_kwargs: dict[str, Any],
        model_name: str,
        encode_kwargs: dict[str, Any] = None,
        *args: dict[str, Any],
        **kwargs: dict[str, Any],
    ):
        """
        Initialize the EmbedDecoratedOperator.

        Args:
            op_args: Positional arguments to pass to the python_callable.
            op_kwargs: Keyword arguments to pass to the python_callable.
            model_name: The name of the model to use for the embedding. Passed to the `SentenceTransformer` constructor.
            encode_kwargs: Keyword arguments to pass to the `encode` method of the SentenceTransformer model.
            *args: Additional positional arguments for the operator.
            **kwargs: Additional keyword arguments for the operator.
        """
        if encode_kwargs is None:
            encode_kwargs = {}

        super().__init__(*args, op_args=op_args, op_kwargs=op_kwargs, **kwargs)

        self.model_name = model_name
        self.encode_kwargs = encode_kwargs

        try:
            import sentence_transformers  # noqa: F401
        except ImportError as e:
            raise ImportError(
                "sentence-transformers is not installed but is required for the embedding operator. Please install it before using the embedding operator."
            ) from e

    def execute(self, context: Context) -> list[float]:
        """
        Execute the embedding operation with the given context.

        Args:
            context: The Airflow context for this task execution.

        Returns:
            A list of floats representing the embedding vector for the input text.
        """
        from sentence_transformers import SentenceTransformer

        text = super().execute(context)
        if not isinstance(text, str):
            raise TypeError("The input text must be a string.")

        model = SentenceTransformer(self.model_name)
        return model.encode(text, **self.encode_kwargs).tolist()
