"""
This package provides an SDK for building LLM workflows and agents using Apache Airflow.

.. deprecated::
    airflow-ai-sdk is no longer actively maintained. Please migrate to
    ``apache-airflow-providers-common-ai``, the official Apache Airflow provider for AI
    and LLM workflows. See the migration guide:
    https://www.astronomer.io/blog/migrating-from-airflow-ai-sdk-to-apache-airflow-s-common-ai-provider/
"""

import warnings
from typing import Any

__version__ = "0.1.8"

warnings.warn(
    "airflow-ai-sdk is deprecated and no longer maintained. Please migrate to "
    "'apache-airflow-providers-common-ai', the official Apache Airflow provider for AI "
    "and LLM workflows. Migration guide: "
    "https://www.astronomer.io/blog/migrating-from-airflow-ai-sdk-to-apache-airflow-s-common-ai-provider/",
    DeprecationWarning,
    stacklevel=2,
)

from airflow_ai_sdk.decorators.agent import agent
from airflow_ai_sdk.decorators.branch import llm_branch
from airflow_ai_sdk.decorators.embed import embed
from airflow_ai_sdk.decorators.llm import llm
from airflow_ai_sdk.models.base import BaseModel

__all__ = ["agent", "llm", "llm_branch", "BaseModel"]


def get_provider_info() -> dict[str, Any]:
    """Get provider information for Airflow.

    Returns:
        A dictionary containing package information and task decorators.
    """
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
            {
                "name": "embed",
                "class-name": "airflow_ai_sdk.decorators.embed.embed",
            },
        ],
    }
