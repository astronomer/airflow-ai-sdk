"""
Compatibility module for different versions of pydantic-ai.

This module handles differences between pydantic-ai versions to ensure
the airflow-ai-sdk works with multiple versions.
"""

try:
    # Try the new location first (pydantic-ai >= 0.0.14)
    from pydantic_ai._utils import _messages
except ImportError:
    try:
        # Fall back to the old location (pydantic-ai < 0.0.14)
        from pydantic_ai.tools import _messages
    except ImportError as e:
        raise ImportError(
            "Could not import _messages from pydantic_ai. "
            "Please ensure you have a compatible version of pydantic-ai installed."
        ) from e

__all__ = ["_messages"]