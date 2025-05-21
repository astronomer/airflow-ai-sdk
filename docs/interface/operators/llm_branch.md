# airflow_ai_sdk.operators.llm_branch

This module provides the LLMBranchDecoratedOperator class for branching DAGs based on
LLM decisions within Airflow tasks.

## LLMBranchDecoratedOperator

Branch a DAG based on the result of an LLM call.

This operator uses an LLM to decide which downstream task to execute next.
It combines the capabilities of an LLM with Airflow's branching functionality.

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
