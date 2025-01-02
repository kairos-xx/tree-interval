
"""Utility functions for Replit operations."""

from pathlib import Path
from typing import Optional


def get_connect_sid() -> Optional[str]:
    """Get Replit connect.sid from the local filesystem.
    
    Returns:
        Optional[str]: The connect.sid if found, None otherwise
    """
    try:
        homedir = Path.home()
        sid_path = homedir / "repl-cli" / "connect.sid"
        if sid_path.exists():
            return sid_path.read_text().strip()
        return None
    except Exception:
        return None
