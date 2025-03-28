"""
This package contains the Airflow AI SDK.
"""

from typing import Any

__version__ = "0.1.1a1"

from airflow_ai_sdk.decorators.agent import agent
from airflow_ai_sdk.decorators.branch import llm_branch
from airflow_ai_sdk.decorators.llm import llm
from airflow_ai_sdk.models.base import BaseModel

__all__ = ["agent", "llm", "llm_branch", "BaseModel"]


def get_provider_info() -> dict[str, Any]:
    return {
        "package-name": "airflow-ai-sdk",
        "name": "Airflow AI SDK",
        "description": "SDK for building LLM workflows and agents using Apache Airflow",
        "versions": [__version__],
        "task-decorators": [
            {
                "name": "agent",
                "class-name": "airflow_ai_sdk.decorators.agent.agent",
            },
            {
                "name": "llm",
                "class-name": "airflow_ai_sdk.decorators.llm.llm",
            },
            {
                "name": "llm_branch",
                "class-name": "airflow_ai_sdk.decorators.branch.llm_branch",
            },
        ],
    }
