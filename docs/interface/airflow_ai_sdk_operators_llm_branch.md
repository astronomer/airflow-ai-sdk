# airflow_ai_sdk.operators.llm_branch

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

## BranchMixIn

Utility helper which handles the branching as one-liner.

## Context

Jinja2 template context for task rendering.

## Enum

Create a collection of name/value pairs.

Example enumeration:

>>> class Color(Enum):
...     RED = 1
...     BLUE = 2
...     GREEN = 3

Access them by:

- attribute access:

  >>> Color.RED
  <Color.RED: 1>

- value lookup:

  >>> Color(1)
  <Color.RED: 1>

- name lookup:

  >>> Color['RED']
  <Color.RED: 1>

Enumerations can be iterated over, and know how many members they have:

>>> len(Color)
3

>>> list(Color)
[<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]

Methods can be added to enumerations, and members can have their own
attributes -- see the documentation for details.

## LLMBranchDecoratedOperator

A decorator that branches the execution of a DAG based on the result of an LLM call.

