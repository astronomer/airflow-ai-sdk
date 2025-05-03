"""
Module that contains the AgentOperator class.
"""

from typing import Any

from airflow_ai_sdk.airflow import Context, _PythonDecoratedOperator
from airflow_ai_sdk.models.base import BaseModel
from airflow_ai_sdk.models.tool import WrappedTool

from sentence_transformers import SentenceTransformer


class EmbedDecoratedOperator(_PythonDecoratedOperator):
    """
    Operator that executes an agent. You can supply a Python callable that returns a string or a list of strings.
    """

    custom_operator_name = "@task.embed"

    def __init__(
        self,
        op_args: list[Any],
        op_kwargs: dict[str, Any],
        text: list[str],
        model: str = "all-MiniLM-L12-v2",
        *args: dict[str, Any],
        **kwargs: dict[str, Any],
    ):
        super().__init__(*args, op_args=op_args, op_kwargs=op_kwargs, **kwargs)

        self.op_args = op_args
        self.op_kwargs = op_kwargs
        self.text = text
        self.model = SentenceTransformer(model)

    def execute(self, context: Context) -> str | dict[str, Any] | list[str]:
        print("Executing embedding")

        prompt = super().execute(context)
        print(f"Prompt: {prompt}")

        try:
            embedding = self.model.encode(self.text, normalize_embeddings=True)[0]
        except Exception as e:
            print(f"Error: {e}")
            raise e

        return embedding.tolist()
