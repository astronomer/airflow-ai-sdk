"""
Tests for the LLMBranchDecoratedOperator class.
"""

from enum import Enum
from unittest.mock import MagicMock, patch

import pytest
from airflow.utils.context import Context

from airflow_ai_sdk.operators.llm_branch import LLMBranchDecoratedOperator


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
def mock_context():
    """Create a mock context."""
    return MagicMock(spec=Context)


@pytest.fixture
def mock_agent():
    """Create a mock agent."""
    return MagicMock()


@pytest.fixture
def patched_agent_class(mock_agent):
    """Patch the Agent class."""
    with patch("airflow_ai_sdk.operators.llm_branch.Agent") as mock_agent_class:
        mock_agent_class.return_value = mock_agent
        yield mock_agent_class


@pytest.fixture
def patched_super_init():
    """Patch the AgentDecoratedOperator.__init__ method."""
    with patch("airflow_ai_sdk.operators.llm_branch.AgentDecoratedOperator.__init__", return_value=None) as mock_super_init:
        yield mock_super_init


def test_init(base_config, patched_agent_class, patched_super_init, mock_agent):
    """Test initialization of LLMBranchDecoratedOperator."""
    # Create the operator
    operator = LLMBranchDecoratedOperator(
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
    )

    # Verify that the properties were set correctly
    assert operator.model == base_config["model"]
    assert operator.system_prompt == base_config["system_prompt"]
    assert operator.allow_multiple_branches is False
    
    # Verify that AgentDecoratedOperator.__init__ was called with the mock agent
    patched_super_init.assert_called_once()
    args, kwargs = patched_super_init.call_args
    assert kwargs["agent"] == mock_agent
    assert "task_id" in kwargs
    assert "op_args" in kwargs
    assert "op_kwargs" in kwargs
    assert "python_callable" in kwargs


def test_init_with_multiple_branches(base_config, patched_agent_class, patched_super_init, mock_agent):
    """Test initialization with allow_multiple_branches=True."""
    # Create the operator
    operator = LLMBranchDecoratedOperator(
        model=base_config["model"],
        system_prompt=base_config["system_prompt"],
        allow_multiple_branches=True,
        task_id="test_task",
        op_args=base_config["op_args"],
        op_kwargs=base_config["op_kwargs"],
        python_callable=lambda: "test",
    )
    
    # Verify the allow_multiple_branches property was set
    assert operator.allow_multiple_branches is True


def test_execute_with_enum_result(base_config, mock_context, mock_agent):
    """Test execute method with an Enum result."""
    with patch("airflow_ai_sdk.operators.llm_branch.Agent") as mock_agent_class:
        with patch("airflow_ai_sdk.operators.llm_branch.AgentDecoratedOperator.execute") as mock_super_execute:
            # Set up mock agent
            mock_agent_class.return_value = mock_agent
            
            # Mock the result of super().execute
            task_id = "task2"
            mock_super_execute.return_value = task_id
            
            # Mock the do_branch method to return a list of tasks
            mock_do_branch_result = ["task2"]
            
            # Create the operator
            with patch("airflow_ai_sdk.operators.llm_branch.AgentDecoratedOperator"):
                with patch.object(LLMBranchDecoratedOperator, "do_branch", return_value=mock_do_branch_result):
                    operator = LLMBranchDecoratedOperator(
                        model=base_config["model"],
                        system_prompt=base_config["system_prompt"],
                        task_id="test_task",
                        op_args=base_config["op_args"],
                        op_kwargs=base_config["op_kwargs"],
                        python_callable=lambda: "test",
                    )
                    
                    # Set downstream task IDs
                    operator.downstream_task_ids = ["task1", "task2", "task3"]
                    
                    # Call execute
                    result = operator.execute(mock_context)
                    
                    # Verify a new Agent was created with the correct enum result_type
                    assert mock_agent_class.call_count == 2  # Once in __init__ and once in execute
                    
                    # Verify that super().execute was called
                    mock_super_execute.assert_called_once_with(mock_context)
                    
                    # Verify the result
                    assert result == mock_do_branch_result


def test_execute_with_non_string_result(base_config, mock_context, mock_agent):
    """Test execute method with a non-string result that needs to be cast to a string."""
    with patch("airflow_ai_sdk.operators.llm_branch.Agent") as mock_agent_class:
        with patch("airflow_ai_sdk.operators.llm_branch.AgentDecoratedOperator.execute") as mock_super_execute:
            # Set up mock agent
            mock_agent_class.return_value = mock_agent
            
            # Mock the result of super().execute to return a non-string value
            mock_super_execute.return_value = 123
            
            # Mock the do_branch method to return a list of tasks
            mock_do_branch_result = ["task1"]
            
            # Create the operator
            with patch("airflow_ai_sdk.operators.llm_branch.AgentDecoratedOperator"):
                with patch.object(LLMBranchDecoratedOperator, "do_branch", return_value=mock_do_branch_result) as mock_do_branch:
                    operator = LLMBranchDecoratedOperator(
                        model=base_config["model"],
                        system_prompt=base_config["system_prompt"],
                        task_id="test_task",
                        op_args=base_config["op_args"],
                        op_kwargs=base_config["op_kwargs"],
                        python_callable=lambda: "test",
                    )
                    
                    # Set downstream task IDs
                    operator.downstream_task_ids = ["task1", "task2", "task3"]
                    
                    # Call execute
                    result = operator.execute(mock_context)
                    
                    # Verify that do_branch was called with the string representation
                    mock_do_branch.assert_called_once_with(mock_context, "123")
                    
                    # Verify the result
                    assert result == mock_do_branch_result