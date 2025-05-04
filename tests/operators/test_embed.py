import pytest
from unittest.mock import patch, MagicMock
from airflow_ai_sdk.airflow import _PythonDecoratedOperator
from airflow_ai_sdk.operators.embed import EmbedDecoratedOperator


@patch.object(_PythonDecoratedOperator, "execute", return_value="hello world")
@patch("airflow_ai_sdk.operators.embed.SentenceTransformer")
def test_execute_returns_vector(mock_sentence_transformer, mock_super_execute):
    test_instance = MagicMock()
    test_array = MagicMock()
    test_array.tolist.return_value = [0.1, 0.2, 0.3]
    test_instance.encode.return_value = test_array
    mock_sentence_transformer.return_value = test_instance

    op = EmbedDecoratedOperator(
        task_id="embed_test",
        python_callable=lambda: "test",
        op_args=None,
        op_kwargs=None,
        model_name="test-model",
    )

    vec = op.execute(context=None)

    mock_super_execute.assert_called_once_with(op, None)
    mock_sentence_transformer.assert_called_once_with("test-model")
    test_instance.encode.assert_called_once_with("hello world", normalize_embeddings=True)
    assert vec == [0.1, 0.2, 0.3]


@patch.object(_PythonDecoratedOperator, "execute", return_value=123)
def test_execute_type_error_on_non_str(mock_super_execute):
    op = EmbedDecoratedOperator(
        task_id="embed_test",
        python_callable=lambda: "test",
        op_args=None,
        op_kwargs=None,
        model_name="test-model",
    )
    with pytest.raises(TypeError, match="Attribute text must be of type str"):
        op.execute(context=None)
