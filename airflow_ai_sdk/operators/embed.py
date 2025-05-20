"""
Module that contains the EmbedOperator class.
"""

from typing import Any

from airflow_ai_sdk.airflow import Context, _PythonDecoratedOperator


class EmbedDecoratedOperator(_PythonDecoratedOperator):
    """Operator that builds embeddings for text.

    Example:
        >>> from airflow_ai_sdk.operators.embed import EmbedDecoratedOperator

        >>> def produce_text() -> str:
        ...     return "document"

        >>> operator = EmbedDecoratedOperator(
        ...     task_id="embed",
        ...     python_callable=produce_text,
        ...     op_args=[],
        ...     op_kwargs={},
        ...     model_name="all-MiniLM-L12-v2",
        ... )
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
        Args:
            model_name: The name of the model to use for the embedding. Passed to the `SentenceTransformer` constructor.
            encode_kwargs: Keyword arguments to pass to the `encode` method of the SentenceTransformer model.
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
        print("Executing embedding")
        text = super().execute(context)
        if not isinstance(text, str):
            raise TypeError("Attribute `text` must be of type `str`")
        try:
            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer(self.model_name)
            embedding = model.encode(text, **self.encode_kwargs)
        except Exception as e:
            print(f"Error: {e}")
            raise e

        return embedding.tolist()
