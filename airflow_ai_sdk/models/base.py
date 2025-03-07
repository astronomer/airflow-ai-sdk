"""
This module contains a base class for all models. We need this because
Airflow requires explicit serialization of all task inputs and outputs.
"""

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    """
    Base class for all models. Mostly reserving this for future use.
    """
