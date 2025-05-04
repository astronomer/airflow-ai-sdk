"""
Module that contains the EmbedOperator class.
"""

from typing import Any

from sentence_transformers import SentenceTransformer

from airflow_ai_sdk.airflow import Context, _PythonDecoratedOperator


class EmbedDecoratedOperator(_PythonDecoratedOperator):
    """
    Operator that builds embeddings for some text.
    """

    custom_operator_name = "@task.embed"

    def __init__(
        self,
        op_args: Any,
        op_kwargs: Any,
        model_name: str,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, op_args=op_args, op_kwargs=op_kwargs, **kwargs)

        self.model_name = model_name

    def execute(self, context: Context) -> list[float]:
        print("Executing embedding")
        text = super().execute(context)
        if not isinstance(text, str):
            raise TypeError("Attribute `text` must be of type `str`")
        try:
            model = SentenceTransformer(self.model_name)
            embedding = model.encode(text, normalize_embeddings=True)
        except Exception as e:
            print(f"Error: {e}")
            raise e

        return embedding.tolist()
