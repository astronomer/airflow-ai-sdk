# airflow_ai_sdk.operators.llm_branch

Module that contains the AgentOperator class.

## LLMBranchDecoratedOperator

Branch a DAG based on the result of an LLM call.

Example:
    ```python
    from airflow_ai_sdk.operators.llm_branch import LLMBranchDecoratedOperator

    def make_prompt() -> str:
        return "Choose"

    operator = LLMBranchDecoratedOperator(
        task_id="branch",
        python_callable=make_prompt,
        model="o3-mini",
        system_prompt="Return 'a' or 'b'",
    )
    ```

