"""
This module provides a base class for all models in the SDK. The base class ensures
proper serialization of task inputs and outputs as required by Airflow.
"""

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    """
    Base class for all models in the SDK.

    This class extends Pydantic's BaseModel to provide a common foundation for all
    models used in the SDK. It ensures proper serialization of task inputs and outputs
    as required by Airflow.

    Example:

    ```python
    from airflow_ai_sdk.models.base import BaseModel

    class MyModel(BaseModel):
        name: str
        value: int
    ```
    """
