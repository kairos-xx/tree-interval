"""Tree Visualization Configuration Module."""

from dataclasses import dataclass


def get_terminal_width() -> int:
    """Get the width of the terminal window."""
    try:
        from shutil import get_terminal_size
        return get_terminal_size().columns
    except Exception:
        return 80  # Default fallback width


@dataclass
class VisualizationConfig:
    """Configuration for tree visualization."""
    terminal_size: int = get_terminal_width()
    show_info: bool = True
    show_size: bool = True
    show_children_count: bool = False
    position_format: str = "range"  # 'range', 'position', or 'tuple'