"""
Tests that all imports from airflow.py resolve correctly.
"""

import pytest


def test_imports_resolve():
    """Test that all imports from airflow.py can be imported successfully."""
    try:
        from airflow_ai_sdk.airflow import (
            Context,
            task_decorator_factory,
            TaskDecorator,
            _PythonDecoratedOperator,
            BranchMixIn,
        )
        # If we get here, imports resolved successfully
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import from airflow.py: {e}")
