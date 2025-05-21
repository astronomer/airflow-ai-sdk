import pytest
import sys
import importlib
from unittest.mock import patch, MagicMock, call
from airflow_ai_sdk.airflow import _PythonDecoratedOperator, task_decorator_factory
from airflow_ai_sdk.operators.embed import EmbedDecoratedOperator
from airflow_ai_sdk.decorators.embed import embed

class StubArray:
    def __init__(self, data):
        self._data = data
    def tolist(self):
        return self._data

class StubModel:
    def __init__(self, name):
        self.name = name

    def encode(self, text, **kwargs):
        # Store kwargs for assertion
        self.last_encode_kwargs = kwargs
        return StubArray([0.1, 0.2, 0.3])

@patch.object(_PythonDecoratedOperator, "execute", autospec=True)
@patch("sentence_transformers.SentenceTransformer", autospec=True)
def test_execute_returns_vector(mock_sentence_transformer, mock_super_execute):
    mock_super_execute.return_value = "hello world"
    mock_model = StubModel("test-model")
    mock_sentence_transformer.return_value = mock_model

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
@patch("sentence_transformers.SentenceTransformer", autospec=True)
def test_execute_with_encode_kwargs(mock_sentence_transformer, mock_super_execute):
    mock_super_execute.return_value = "hello world"
    mock_model = StubModel("test-model")
    mock_sentence_transformer.return_value = mock_model

    encode_kwargs = {
        "normalize_embeddings": True,
        "batch_size": 32,
        "show_progress_bar": False
    }

    op = EmbedDecoratedOperator(
        task_id="embed_test",
        python_callable=lambda: "ignored",
        op_args=None,
        op_kwargs=None,
        model_name="test-model",
        encode_kwargs=encode_kwargs
    )

    vec = op.execute(context=None)

    mock_super_execute.assert_called_once_with(op, None)
    mock_sentence_transformer.assert_called_once_with("test-model")
    assert vec == [0.1, 0.2, 0.3]
    # Verify encode_kwargs were passed correctly
    assert mock_model.last_encode_kwargs == encode_kwargs

@patch.object(_PythonDecoratedOperator, "execute", autospec=True)
def test_execute_raises_error_on_non_str(mock_super_execute):
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

@patch("airflow_ai_sdk.decorators.embed.task_decorator_factory")
def test_embed_decorator(mock_task_decorator_factory):
    # Setup mock
    mock_decorator = MagicMock()
    mock_task_decorator_factory.return_value = mock_decorator

    # Test with custom model name
    custom_model = "custom-model"
    result = embed(model_name=custom_model)

    # Verify decorator factory was called correctly
    mock_task_decorator_factory.assert_called_once_with(
        decorated_operator_class=EmbedDecoratedOperator,
        model_name=custom_model
    )
    # Verify the result is the mock decorator
    assert result == mock_decorator

@patch("airflow_ai_sdk.decorators.embed.task_decorator_factory")
def test_embed_decorator_with_default_model(mock_task_decorator_factory):
    # Reset mock
    mock_task_decorator_factory.reset_mock()

    # Setup mock
    mock_decorator = MagicMock()
    mock_task_decorator_factory.return_value = mock_decorator

    # Call with default model name
    result = embed()

    # Verify decorator factory was called with default model name
    mock_task_decorator_factory.assert_called_once_with(
        decorated_operator_class=EmbedDecoratedOperator,
        model_name="all-MiniLM-L12-v2"  # Default value defined in embed.py
    )
    # Verify the result is the mock decorator
    assert result == mock_decorator

@patch("airflow_ai_sdk.decorators.embed.task_decorator_factory")
def test_embed_decorator_passes_additional_kwargs(mock_task_decorator_factory):
    # Reset mock
    mock_task_decorator_factory.reset_mock()

    # Setup mock
    mock_decorator = MagicMock()
    mock_task_decorator_factory.return_value = mock_decorator

    # Call with additional kwargs
    additional_kwargs = {
        "task_id": "custom_task_id",
        "pool": "custom_pool",
        "priority_weight": 10,
        "encode_kwargs": {"normalize_embeddings": True}
    }

    result = embed(model_name="custom-model", **additional_kwargs)

    # Verify decorator factory was called with all kwargs
    expected_kwargs = {
        "decorated_operator_class": EmbedDecoratedOperator,
        "model_name": "custom-model",
        **additional_kwargs
    }
    mock_task_decorator_factory.assert_called_once_with(**expected_kwargs)

    # Verify the result is the mock decorator
    assert result == mock_decorator

def test_import_error_when_sentence_transformers_not_installed():
    # Mock that sentence_transformers is not installed
    with patch.dict(sys.modules, {'sentence_transformers': None}):
        # Make sure the import attempt fails
        with pytest.raises(ImportError) as excinfo:
            # Force module reload to trigger the import check
            import importlib
            if 'airflow_ai_sdk.operators.embed' in sys.modules:
                importlib.reload(sys.modules['airflow_ai_sdk.operators.embed'])
            else:
                import airflow_ai_sdk.operators.embed

            # Try to create an operator - this should raise ImportError
            EmbedDecoratedOperator(
                task_id="embed_test",
                python_callable=lambda: "ignored",
                op_args=None,
                op_kwargs=None,
                model_name="test-model",
            )

        # Check for expected error message
        error_msg = str(excinfo.value)
        assert "sentence-transformers is not installed" in error_msg

class ExceptionRaisingModel:
    def __init__(self, name):
        self.name = name

    def encode(self, text, **kwargs):
        raise ValueError("Test exception from model encoding")

@patch.object(_PythonDecoratedOperator, "execute", autospec=True)
@patch("sentence_transformers.SentenceTransformer", autospec=True)
def test_model_exception_handling(mock_sentence_transformer, mock_super_execute):
    # Setup mocks
    mock_super_execute.return_value = "hello world"
    mock_sentence_transformer.return_value = ExceptionRaisingModel("test-model")

    op = EmbedDecoratedOperator(
        task_id="embed_test",
        python_callable=lambda: "ignored",
        op_args=None,
        op_kwargs=None,
        model_name="test-model",
    )

    # The operator should re-raise the exception
    with pytest.raises(ValueError) as excinfo:
        op.execute(context=None)

    # Check that the exception came from the model
    assert "Test exception from model encoding" in str(excinfo.value)

    # Verify the proper methods were called
    mock_super_execute.assert_called_once_with(op, None)
    mock_sentence_transformer.assert_called_once_with("test-model")

@patch.object(_PythonDecoratedOperator, "execute", autospec=True)
@patch("sentence_transformers.SentenceTransformer", autospec=True)
def test_non_string_input_types(mock_sentence_transformer, mock_super_execute):
    mock_model = StubModel("test-model")
    mock_sentence_transformer.return_value = mock_model

    op = EmbedDecoratedOperator(
        task_id="embed_test",
        python_callable=lambda: "ignored",
        op_args=None,
        op_kwargs=None,
        model_name="test-model",
    )

    # Test input types that aren't strings and should cause TypeError
    non_string_inputs = [
        123,                # int
        1.23,               # float
        True,               # bool
        ["item1", "item2"], # list
        {"key": "value"},   # dict
        (1, 2, 3),          # tuple
        None                # None
    ]

    for input_val in non_string_inputs:
        mock_super_execute.reset_mock()
        mock_super_execute.return_value = input_val

        with pytest.raises(TypeError) as excinfo:
            op.execute(context=None)

        error_msg = str(excinfo.value)
        assert "text" in error_msg.lower()
        assert "str" in error_msg.lower()
        mock_super_execute.assert_called_once_with(op, None)
