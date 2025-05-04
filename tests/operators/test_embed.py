import pytest
from unittest.mock import patch, MagicMock
from airflow_ai_sdk.airflow import _PythonDecoratedOperator
from airflow_ai_sdk.operators.embed import EmbedDecoratedOperator

class StubArray:
    def __init__(self, data):
        self._data = data
    def tolist(self):
        return self._data

class StubModel:
    def __init__(self, name):
        assert name == "test-model"
    def encode(self, text, normalize_embeddings):
        assert normalize_embeddings is True
        return StubArray([0.1, 0.2, 0.3])

@patch.object(_PythonDecoratedOperator, "execute", autospec=True)
@patch("airflow_ai_sdk.operators.embed.SentenceTransformer", autospec=True)
def test_execute_returns_vector(mock_sentence_transformer, mock_super_execute):

    mock_super_execute.return_value = "hello world"
    mock_sentence_transformer.return_value = StubModel("test-model")

    op = EmbedDecoratedOperator(
        task_id="embed_test",
        python_callable=lambda: "ignored",
        op_args=None,
        op_kwargs=None,
        model_name="test-model",
    )

    vec = op.execute(context=None)

    mock_super_execute.assert_called_once_with(op, None)
    mock_sentence_transformer.assert_called_once_with("test-model")
    assert vec == [0.1, 0.2, 0.3]

@patch.object(_PythonDecoratedOperator, "execute", autospec=True)
def test_execute_type_error_on_non_str(mock_super_execute):

    mock_super_execute.return_value = 12345

    op = EmbedDecoratedOperator(
        task_id="embed_test",
        python_callable=lambda: "ignored",
        op_args=None,
        op_kwargs=None,
        model_name="test-model",
    )

    with pytest.raises(TypeError) as excinfo:
        op.execute(context=None)
    msg = str(excinfo.value)
    assert "text" in msg.lower()
    assert "str" in msg.lower()
