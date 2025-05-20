# airflow_ai_sdk.airflow

This contains any imports we need to make to support both Airflow 2.x and 3.x.

## BranchMixIn

Utility helper which handles the branching as one-liner.

## Context

Jinja2 template context for task rendering.

## TaskDecorator

Type declaration for ``task_decorator_factory`` return type.

## task_decorator_factory

Generate a wrapper that wraps a function into an Airflow operator.

Can be reused in a single DAG.

:param python_callable: Function to decorate.
:param multiple_outputs: If set to True, the decorated function's return
    value will be unrolled to multiple XCom values. Dict will unroll to XCom
    values with its keys as XCom keys. If set to False (default), only at
    most one XCom value is pushed.
:param decorated_operator_class: The operator that executes the logic needed
    to run the python function in the correct environment.

Other kwargs are directly forwarded to the underlying operator class when
it's instantiated.

