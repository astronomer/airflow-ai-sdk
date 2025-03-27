"""
Tests for the AgentDecoratedOperator class.
"""

from unittest.mock import MagicMock, patch

import pytest
from airflow.utils.context import Context
from pydantic_ai import Tool
from pydantic_ai.agent import AgentRunResult

from airflow_ai_sdk.models.base import BaseModel
from airflow_ai_sdk.operators.agent import AgentDecoratedOperator, WrappedTool


def tool1(input: str) -> str:
    """Tool 1."""
    return f"tool1_result: {input}"

def tool2(input: str) -> str:
    """Tool 2."""
    return f"tool2_result: {input}"


@pytest.fixture
def base_config():
    """Base configuration for tests."""
    return {
        "op_args": [],
        "op_kwargs": {},
    }


@pytest.fixture
def mock_context():
    """Create a mock context."""
    return MagicMock(spec=Context)


@pytest.fixture
def mock_agent_with_tools():
    """Create a mock agent with tools."""
    mock_agent = MagicMock()
    mock_agent._function_tools = {"tool1": Tool(tool1), "tool2": Tool(tool2)}
    return mock_agent


@pytest.fixture
def mock_agent_no_tools():
    """Create a mock agent without tools."""
    mock_agent = MagicMock()
    mock_agent._function_tools = {}
    return mock_agent


@pytest.fixture
def patched_agent_class():
    """Patch the Agent class."""
    with patch("airflow_ai_sdk.operators.agent.Agent") as mock_agent_class:
        yield mock_agent_class


@pytest.fixture
def patched_super_execute():
    """Patch _PythonDecoratedOperator.execute."""
    with patch("airflow_ai_sdk.operators.agent._PythonDecoratedOperator.execute") as mock_super_execute:
        mock_super_execute.return_value = "test_prompt"
        yield mock_super_execute


def test_init(base_config, mock_agent_with_tools):
    """Test the initialization of AgentDecoratedOperator."""
    operator = AgentDecoratedOperator(
        agent=mock_agent_with_tools,
        task_id="test_task",
        python_callable=lambda: "test",
        op_args=base_config["op_args"],
        op_kwargs=base_config["op_kwargs"],
    )

    # Make sure the tools were wrapped by checking the agent's function tools' class
    print(operator.agent._function_tools)
    assert isinstance(operator.agent._function_tools["tool1"], WrappedTool)
    assert isinstance(operator.agent._function_tools["tool2"], WrappedTool)

def test_execute_with_string_result(base_config, mock_context, mock_agent_no_tools):
    """Test execute method with a string result."""
    # Mock the result of run_sync
    mock_result = MagicMock(spec=AgentRunResult)
    mock_result.data = "test_result"
    mock_agent_no_tools.run_sync.return_value = mock_result
    
    # Create the operator
    operator = AgentDecoratedOperator(
        agent=mock_agent_no_tools,
        task_id="test_task",
        python_callable=lambda: "test",
        op_args=base_config["op_args"],
        op_kwargs=base_config["op_kwargs"],
    )
        
    # Call execute
    result = operator.execute(mock_context)
        
    # Verify the result
    assert result == "test_result"


def test_execute_with_base_model_result(base_config, mock_context, mock_agent_no_tools):
    """Test execute method with a BaseModel result."""
    # Create a test model
    class TestModel(BaseModel):
        field1: str
        field2: int
    
    test_model = TestModel(field1="test", field2=42)
    
    # Mock the result of run_sync
    mock_result = MagicMock()
    mock_result.data = test_model
    mock_agent_no_tools.run_sync.return_value = mock_result
    
    # Create the operator
    operator = AgentDecoratedOperator(
        agent=mock_agent_no_tools,
        task_id="test_task",
        python_callable=lambda: "test",
        op_args=base_config["op_args"],
        op_kwargs=base_config["op_kwargs"],
        )
        
    # Call execute
    result = operator.execute(mock_context)
        
    # Verify the result
    assert result == {"field1": "test", "field2": 42}


def test_execute_with_error(base_config, mock_context, mock_agent_no_tools):
    """Test execute method when an error occurs."""
    # Configure the mock agent's run_sync to raise an exception
    error_message = "Test error"
    mock_agent_no_tools.run_sync.side_effect = ValueError(error_message)
    
    # Create the operator
    operator = AgentDecoratedOperator(
        agent=mock_agent_no_tools,
        task_id="test_task",
        python_callable=lambda: "test",
        op_args=base_config["op_args"],
        op_kwargs=base_config["op_kwargs"],
    )
        
    # Call execute
    with pytest.raises(ValueError, match=error_message):
        operator.execute(mock_context)
    
    # Verify that run_sync was called
    mock_agent_no_tools.run_sync.assert_called_once_with("test")
