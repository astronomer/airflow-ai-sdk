# airflow_ai_sdk.operators.agent

Module that contains the AgentOperator class.

## AgentDecoratedOperator

Operator that executes a :class:`pydantic_ai.Agent`.

Example:
    ```python
    from pydantic_ai import Agent
    from airflow_ai_sdk.operators.agent import AgentDecoratedOperator

    def prompt() -> str:
        return "Hello"

    operator = AgentDecoratedOperator(
        task_id="example",
        python_callable=prompt,
        agent=Agent(model="o3-mini", system_prompt="Say hello"),
        op_args=[],
        op_kwargs={},
    )
    ```

