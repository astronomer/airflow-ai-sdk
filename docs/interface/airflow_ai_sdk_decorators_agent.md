# airflow_ai_sdk.decorators.agent

This module contains the decorators for the agent.

## Agent

Class for defining "agents" - a way to have a specific type of "conversation" with an LLM.

Agents are generic in the dependency type they take [`AgentDepsT`][pydantic_ai.tools.AgentDepsT]
and the result data type they return, [`ResultDataT`][pydantic_ai.result.ResultDataT].

By default, if neither generic parameter is customised, agents have type `Agent[None, str]`.

Minimal usage example:

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')
result = agent.run_sync('What is the capital of France?')
print(result.data)
#> Paris
```

## AgentDecoratedOperator

Operator that executes an agent. You can supply a Python callable that returns a string or a list of strings.

## Any

Special type indicating an unconstrained type.

- Any is compatible with every type.
- Any assumed to have all methods.
- All values assumed to be instances of Any.

Note that all the above statements are true from the point of view of
static type checkers. At runtime, Any should not be used with instance
checks.

## agent

Decorator to make agent calls.

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

