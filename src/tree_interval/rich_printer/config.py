"""Configuration for Rich tree printer."""

from dataclasses import dataclass

from rich.style import Style


@dataclass
class RichPrintConfig:
    """Configuration for Rich tree visualization."""

    show_info: bool = True
    show_size: bool = True
    show_position: bool = True
    indent_size: int = 2
    root_style: Style = Style(color="green", bold=True)
    node_style: Style = Style(color="blue")
    leaf_style: Style = Style(color="cyan")
    info_style: Style = Style(color="yellow", italic=True)
    guide_style: Style = Style(color="grey70")
    selected_style: Style = Style(color="red", bold=True)
