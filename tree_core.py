
"""
Core tree data structures.

This module contains the core Tree and Leaf classes used across the project.
"""

from dataclasses import dataclass, field
from json import dumps, loads
from typing import Any, Dict, Generic, List, NamedTuple, Optional, TypeVar, Union

T = TypeVar('T')
L = TypeVar('L', bound='Leaf')

class Position:
    def __init__(self, 
                 start: Optional[int] = None,
                 end: Optional[int] = None,
                 info: Optional[Any] = None):
        self.start = start
        self.end = end
        self.info = info
        self._lineno: Optional[int] = None
        self._end_lineno: Optional[int] = None
        self._col_offset: Optional[int] = None
        self._end_col_offset: Optional[int] = None

    @property
    def lineno(self) -> Optional[int]:
        return self._lineno

    @lineno.setter
    def lineno(self, value: Optional[int]) -> None:
        self._lineno = value

    @property
    def end_lineno(self) -> Optional[int]:
        return self._end_lineno

    @end_lineno.setter
    def end_lineno(self, value: Optional[int]) -> None:
        self._end_lineno = value

    @property
    def col_offset(self) -> Optional[int]:
        return self._col_offset

    @col_offset.setter
    def col_offset(self, value: Optional[int]) -> None:
        self._col_offset = value

    @property
    def end_col_offset(self) -> Optional[int]:
        return self._end_col_offset

    @end_col_offset.setter
    def end_col_offset(self, value: Optional[int]) -> None:
        self._end_col_offset = value

    @property
    def absolute_start(self) -> Optional[int]:
        return self.start if self.start is not None else None

    @property
    def absolute_end(self) -> Optional[int]:
        return self.end if self.end is not None else None

class Leaf:
    """A node in the tree structure containing position and information data."""
    def __init__(self, 
                 position: Union[Position, tuple[int, int, Any], int],
                 end: Optional[int] = None,
                 info: Optional[Any] = None) -> None:
        if isinstance(position, Position):
            self.position = position
        elif isinstance(position, tuple):
            self.position = Position(*position)
        else:
            self.position = Position(position, end, info)
            
        self.parent: Optional[Leaf] = None
        self.children: List[Leaf] = []

    @property
    def start(self) -> Optional[int]:
        return self.position.start

    @property
    def end(self) -> Optional[int]:
        return self.position.end
        
    @property
    def info(self) -> Optional[Any]:
        return self.position.info

    @property
    def size(self) -> Optional[int]:
        if self.start is None or self.end is None:
            return None
        return self.end - self.start

    def add_child(self, child: L) -> None:
        """Add a child node to this leaf."""
        child.parent = self
        self.children.append(child)

    def find_best_match(self, start: int, end: int) -> Optional[L]:
        """Find the leaf that best matches the given range."""
        if self.start is None or self.end is None:
            return None
            
        if start >= self.start and end <= self.end:
            best_match = self
            for child in self.children:
                child_match = child.find_best_match(start, end)
                if child_match and child_match.size and best_match.size:
                    if child_match.size < best_match.size:
                        best_match = child_match
            return best_match
        return None

    def find_common_ancestor(self, other: L) -> Optional[L]:
        """Find the first common ancestor between this leaf and another."""
        if not other:
            return None
            
        this_ancestors = set()
        current = self
        while current:
            this_ancestors.add(current)
            current = current.parent

        current = other
        while current:
            if current in this_ancestors:
                return current
            current = current.parent
        return None

    def find_first_multi_child_ancestor(self) -> Optional[L]:
        """Find the first ancestor that has multiple children."""
        current = self.parent
        while current:
            if len(current.children) > 1:
                return current
            current = current.parent
        return None
