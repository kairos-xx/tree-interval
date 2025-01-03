
"""Core interval module."""

from dataclasses import dataclass
from typing import Any, Generic, List, Optional, TypeVar, Union

T = TypeVar('T')

@dataclass
class Position:
    """Position with line and column information."""
    
    start: Optional[int]
    end: Optional[int]
    selected: bool = False

    def __post_init__(self) -> None:
        self._lineno: Optional[int] = None
        self._end_lineno: Optional[int] = None
        self._col_offset: Optional[int] = None
        self._end_col_offset: Optional[int] = None


class Tree(Generic[T]):
    """Tree structure with position-aware nodes."""

    def __init__(self, source: T) -> None:
        self.source = source
        self.root: Optional['Leaf'] = None

    def add_leaf(self, leaf: 'Leaf') -> None:
        """Add a leaf to the tree."""
        if not self.root:
            self.root = leaf
            return
        
        if leaf.start is None or leaf.end is None:
            return

        best_match = self.root.find_best_match(leaf.start, leaf.end)
        if best_match:
            best_match.add_child(leaf)


class Leaf:
    """Node in the tree structure."""

    def __init__(
        self,
        position: Union[Position, tuple, int],
        info: Any = None,
        end: Optional[int] = None,
    ) -> None:
        if isinstance(position, Position):
            self.position = position
        elif isinstance(position, tuple):
            self.position = Position(position[0], position[1])
        else:
            self.position = Position(position, end)

        self.info = info
        self.parent: Optional[Leaf] = None
        self.children: List[Leaf] = []

    @property
    def start(self) -> Optional[int]:
        """Get start position."""
        return self.position.start

    @property
    def end(self) -> Optional[int]:
        """Get end position."""
        return self.position.end

    def add_child(self, child: 'Leaf') -> None:
        """Add a child node."""
        child.parent = self
        self.children.append(child)

    def find_best_match(
        self,
        start: int,
        end: int,
        best_match_distance: Optional[float] = None
    ) -> Optional['Leaf']:
        """Find best matching node for given range."""
        if self.start is None or self.end is None:
            return None

        if best_match_distance is None:
            best_match_distance = float('inf')

        current_distance = abs(start - self.start) + abs(end - self.end)
        best_match = self if current_distance < best_match_distance else None

        for child in self.children:
            child_match = child.find_best_match(start, end, current_distance)
            if child_match:
                best_match = child_match

        return best_match
