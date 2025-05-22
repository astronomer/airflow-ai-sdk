# airflow_ai_sdk.models.tool

This module provides a wrapper around pydantic_ai.Tool for better observability in Airflow.

## WrappedTool

Wrapper around `pydantic_ai.Tool` for better observability in Airflow.

This class extends the `pydantic_ai.Tool` class to provide enhanced logging
capabilities in Airflow. It wraps tool calls and results in log groups for
better visibility in the Airflow UI.

Example:

```python
from airflow_ai_sdk.models.tool import WrappedTool
from pydantic_ai import Tool

tool = Tool(my_function, name="my_tool")
wrapped_tool = WrappedTool.from_pydantic_tool(tool)
```
