
"""Configuration classes for tree visualization."""

from dataclasses import dataclass

@dataclass
class VisualizationConfig:
    """Configuration for tree visualization."""
    show_info: bool = True
    show_size: bool = True
    show_children_count: bool = False
    position_format: str = 'range'  # 'range', 'position', or 'tuple'
