"""
Compatibility module for different versions of pydantic-ai.

This module handles differences between pydantic-ai versions to ensure
the airflow-ai-sdk works with multiple versions.
"""

try:
    # Try importing from the messages module (current pydantic-ai structure)
    from pydantic_ai import messages as _messages
except ImportError:
    try:
        # Fall back to the old location (older pydantic-ai versions)
        from pydantic_ai.tools import _messages
    except ImportError as e:
        raise ImportError(
            "Could not import messages from pydantic_ai. "
            "Please ensure you have a compatible version of pydantic-ai installed."
        ) from e

__all__ = ["_messages"]