# airflow_ai_sdk.decorators.llm

This module contains the decorators for the llm decorator.

## Any

Special type indicating an unconstrained type.

- Any is compatible with every type.
- Any assumed to have all methods.
- All values assumed to be instances of Any.

Note that all the above statements are true from the point of view of
static type checkers. At runtime, Any should not be used with instance
checks.

## BaseModel

Base class for all models. Mostly reserving this for future use.

## LLMDecoratedOperator

Provides an abstraction on top of the Agent class. Not as powerful as the Agent class, but
provides a simpler interface.

## llm

Decorator to make LLM calls.

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

