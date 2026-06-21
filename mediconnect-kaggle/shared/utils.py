"""
Shared Utilities
================
Common helper functions used across all agents.
"""
import json
from datetime import datetime


def format_json(data: dict) -> str:
    """Format dictionary as pretty-printed JSON."""
    return json.dumps(data, indent=2, ensure_ascii=False)


def get_timestamp() -> str:
    """Get current ISO timestamp."""
    return datetime.now().isoformat()


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to maximum length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def safe_get(dictionary: dict, key: str, default=None):
    """Safely get value from dictionary with default."""
    return dictionary.get(key, default)


def validate_required_fields(data: dict, required: list) -> tuple:
    """
    Validate that all required fields are present.

    Returns:
        (is_valid: bool, missing_fields: list)
    """
    missing = [field for field in required if field not in data or data[field] is None]
    return len(missing) == 0, missing
