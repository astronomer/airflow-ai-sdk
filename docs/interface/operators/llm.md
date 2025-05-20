# airflow_ai_sdk.operators.llm

Module that contains the AgentOperator class.

## LLMDecoratedOperator

Simpler interface for performing a single LLM call.

Example:
    ```python
    from airflow_ai_sdk.operators.llm import LLMDecoratedOperator

    def make_prompt() -> str:
        return "Hello"

    operator = LLMDecoratedOperator(
        task_id="llm",
        python_callable=make_prompt,
        model="o3-mini",
        system_prompt="Reply politely",
    )
    ```

