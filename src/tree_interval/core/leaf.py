
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union
from .interval_core import Position

class Leaf:
    """A node in the tree structure containing position and information data."""

    def __init__(
        self,
        position: Union[Position, tuple[int, int, Any], int],
        end: Optional[int] = None,
        info: Optional[Any] = None,
    ) -> None:
        if isinstance(position, Position):
            self.position = position
        elif isinstance(position, tuple):
            self.position = Position(*position)
        else:
            self.position = Position(position, end, info)

        self.parent: Optional["Leaf"] = None
        self.children: List["Leaf"] = []

    # ...rest of the Leaf class implementation...
