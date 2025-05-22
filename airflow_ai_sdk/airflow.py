"""
This module provides compatibility layer for Airflow 2.x and 3.x by importing the necessary
decorators, operators, and context utilities from the appropriate Airflow version.
"""

try:
    # 3.x
    from airflow.providers.standard.decorators.python import _PythonDecoratedOperator
    from airflow.providers.standard.operators.branch import BranchMixIn
    from airflow.sdk.bases.decorator import TaskDecorator, task_decorator_factory
    from airflow.sdk.definitions.context import Context
except ImportError:
    # 2.x
    from airflow.decorators.base import (
        TaskDecorator,
        task_decorator_factory,
    )
    from airflow.decorators.python import _PythonDecoratedOperator
    from airflow.operators.python import BranchMixIn
    from airflow.utils.context import Context

__all__ = [
    "Context",
    "task_decorator_factory",
    "TaskDecorator",
    "_PythonDecoratedOperator",
    "BranchMixIn",
]
