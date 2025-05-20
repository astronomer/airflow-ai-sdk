# airflow_ai_sdk.operators.agent

Module that contains the AgentOperator class.

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

## BaseModel

Base class for all models. Mostly reserving this for future use.

## Context

Jinja2 template context for task rendering.

## WrappedTool

Wrapper around the pydantic_ai.Tool class that prints the tool call and the result
in an airflow log group for better observability.

