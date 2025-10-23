"""Command-line UI helpers for alphavox Dashboard."""

from typing import Dict, Any


def render_dashboard(status: Dict[str, Any]) -> str:
    """Return a textual representation of alphavox's status."""
    lines = [
        "alphavox Dashboard",
        "==============",
        f"Status: {status.get('alphavox_status', 'unknown')}",
        f"API Host: {status.get('settings', {}).get('api_host', 'n/a')}",
    ]
    return "\n".join(lines)
