"""
Tests for the LLMDecoratedOperator class.
"""

from unittest.mock import MagicMock, patch

import pytest
from _pytest.recwarn import WarningsRecorder
from pydantic import BaseModel
from pydantic_ai.models import Model

from airflow_ai_sdk.operators.llm import LLMDecoratedOperator


@pytest.fixture
def base_config():
    """Base configuration for tests."""
    return {
        "model": "gpt-4",
        "system_prompt": "You are a helpful assistant.",
        "op_args": [],
        "op_kwargs": {},
    }


@pytest.fixture
def mock_agent():
    """Create a mock agent."""
    return MagicMock()


@pytest.fixture
def patched_agent_class(mock_agent):
    """Patch the Agent class."""
    with patch("airflow_ai_sdk.operators.llm.Agent") as mock_agent_class:
        mock_agent_class.return_value = mock_agent
        yield mock_agent_class


@pytest.fixture
def patched_super_init():
    """Patch the AgentDecoratedOperator.__init__ method."""
    with patch("airflow_ai_sdk.operators.llm.AgentDecoratedOperator.__init__", return_value=None) as mock_super_init:
        yield mock_super_init


def test_init_with_default_output_type(base_config, patched_agent_class, patched_super_init, mock_agent):
    """Test initialization with default output type (str)."""
    # Create the operator
    operator = LLMDecoratedOperator(
        model=base_config["model"],
        system_prompt=base_config["system_prompt"],
        task_id="test_task",
        op_args=base_config["op_args"],
        op_kwargs=base_config["op_kwargs"],
        python_callable=lambda: "test",
    )

    # Verify that Agent was created with the correct arguments
    patched_agent_class.assert_called_once_with(
        model=base_config["model"],
        system_prompt=base_config["system_prompt"],
        output_type=str,
    )

    # Verify that AgentDecoratedOperator.__init__ was called with the mock agent
    patched_super_init.assert_called_once()
    args, kwargs = patched_super_init.call_args
    assert kwargs["agent"] == mock_agent
    assert "task_id" in kwargs
    assert "op_args" in kwargs
    assert "op_kwargs" in kwargs
    assert "python_callable" in kwargs


def test_init_with_custom_output_type(base_config, patched_agent_class, patched_super_init, mock_agent):
    """Test initialization with custom output type."""

    # Create a test model
    class TestModel(BaseModel):
        field1: str
        field2: int

    # Create the operator
    operator = LLMDecoratedOperator(
        model=base_config["model"],
        system_prompt=base_config["system_prompt"],
        output_type=TestModel,
        task_id="test_task",
        op_args=base_config["op_args"],
        op_kwargs=base_config["op_kwargs"],
        python_callable=lambda: "test",
    )

    # Verify that Agent was created with the correct arguments
    patched_agent_class.assert_called_once_with(
        model=base_config["model"],
        system_prompt=base_config["system_prompt"],
        output_type=TestModel,
    )

    # Verify that AgentDecoratedOperator.__init__ was called with the mock agent
    patched_super_init.assert_called_once()
    args, kwargs = patched_super_init.call_args
    assert kwargs["agent"] == mock_agent
    assert "task_id" in kwargs
    assert "op_args" in kwargs
    assert "op_kwargs" in kwargs
    assert "python_callable" in kwargs


def test_init_with_model_object(base_config, patched_agent_class, patched_super_init, mock_agent):
    """Test initialization with a Model object instead of a string."""
    # Create a mock model object
    mock_model = MagicMock(spec=Model)

    # Create the operator
    operator = LLMDecoratedOperator(
        model=mock_model,
        system_prompt=base_config["system_prompt"],
        task_id="test_task",
        op_args=base_config["op_args"],
        op_kwargs=base_config["op_kwargs"],
        python_callable=lambda: "test",
    )

    # Verify that Agent was created with the correct arguments
    patched_agent_class.assert_called_once_with(
        model=mock_model,
        system_prompt=base_config["system_prompt"],
        output_type=str,
    )

    # Verify that AgentDecoratedOperator.__init__ was called with the mock agent
    patched_super_init.assert_called_once()
    args, kwargs = patched_super_init.call_args
    assert kwargs["agent"] == mock_agent
    assert "task_id" in kwargs
    assert "op_args" in kwargs
    assert "op_kwargs" in kwargs
    assert "python_callable" in kwargs


def test_deprecated_call(base_config, patched_agent_class, patched_super_init, mock_agent):
    """
    Check for a deprecation warning from result_type.
    TODO remove test after removing support for result_type in airflow-ai-sdk 1.0.0.
    """
    with pytest.deprecated_call():
        LLMDecoratedOperator(
            task_id="test",
            system_prompt="Test me",
            model="gpt-4",
            op_args=[],
            op_kwargs={},
            python_callable=lambda: "test",
            result_type=str,
        )

    with pytest.raises(ValueError):
        LLMDecoratedOperator(
            task_id="test",
            system_prompt="Test me",
            model="gpt-4",
            op_args=[],
            op_kwargs={},
            python_callable=lambda: "test",
            result_type=str,
            output_type=str,
        )


def test_no_deprecation_calls(
    recwarn: WarningsRecorder, base_config, patched_agent_class, patched_super_init, mock_agent
):
    """We expect no deprecation warnings using these arguments."""
    LLMDecoratedOperator(
        task_id="test",
        system_prompt="Test me",
        model="gpt-4",
        op_args=[],
        op_kwargs={},
        python_callable=lambda: "test",
        output_type=str,
    )
    assert len(recwarn) == 0
