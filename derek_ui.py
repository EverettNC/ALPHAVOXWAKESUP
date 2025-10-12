"""Command-line UI helpers for Derek Dashboard."""

from typing import Dict, Any


def render_dashboard(status: Dict[str, Any]) -> str:
    """Return a textual representation of Derek's status."""
    lines = [
        "Derek Dashboard",
        "==============",
        f"Status: {status.get('derek_status', 'unknown')}",
        f"API Host: {status.get('settings', {}).get('api_host', 'n/a')}",
    ]
    return "\n".join(lines)
