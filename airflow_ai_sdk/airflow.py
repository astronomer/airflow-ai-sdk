"""
This contains any imports we need to make to support both Airflow 2.x and 3.x.
"""

try:
    # 3.x
    from airflow.providers.standard.decorators.python import _PythonDecoratedOperator
    from airflow.providers.standard.operators.branch import BranchMixIn
    from airflow.sdk.bases.decorator import TaskDecorator, task_decorator_factory
    from airflow.sdk.definitions.context import Context
except ImportError:
    # 2.x
    from airflow.decorators.base import TaskDecorator, task_decorator_factory
    from airflow.operators.python import BranchMixIn, _PythonDecoratedOperator
    from airflow.utils.context import Context

__all__ = [
    "Context",
    "task_decorator_factory",
    "TaskDecorator",
    "_PythonDecoratedOperator",
    "BranchMixIn",
]
