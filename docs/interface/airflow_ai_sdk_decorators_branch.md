# airflow_ai_sdk.decorators.branch

This module contains the decorators for the llm_branch decorator.

## Any

Special type indicating an unconstrained type.

- Any is compatible with every type.
- Any assumed to have all methods.
- All values assumed to be instances of Any.

Note that all the above statements are true from the point of view of
static type checkers. At runtime, Any should not be used with instance
checks.

## LLMBranchDecoratedOperator

A decorator that branches the execution of a DAG based on the result of an LLM call.

## llm_branch

Decorator to make LLM calls and branch the execution of a DAG based on the result.

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

