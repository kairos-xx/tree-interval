
"""Core interval and tree functionality."""

import ast
from dataclasses import dataclass
from json import dumps, loads
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, Union

from tree_interval.core.ast_types import AST_TYPES

T = TypeVar("T")


@dataclass
class Position:
    """Position information for tree nodes."""
    
    def __init__(self, start: Optional[int], end: Optional[int]) -> None:
        self.start = start
        self.end = end
        self._lineno: Optional[int] = None
        self._end_lineno: Optional[int] = None
        self._col_offset: Optional[int] = None 
        self._end_col_offset: Optional[int] = None
        self.selected: bool = False

    @property
    def absolute_start(self) -> int:
        return self.start if self.start is not None else 0

    @property
    def absolute_end(self) -> int:
        return self.end if self.end is not None else 0

    def position_as(self, position_format: str = "default") -> str:
        if position_format == "position":
            return (
                f"Position(start={self.start}, end={self.end}, "
                f"lineno={self._lineno}, end_lineno={self._end_lineno}, "
                f"col_offset={self._col_offset}, "
                f"end_col_offset={self._end_col_offset})"
            )
        elif position_format == "tuple":
            return (
                f"({self.start}, {self.end}, {self._lineno}, "
                f"{self._end_lineno}, {self._col_offset}, {self._end_col_offset})"
            )
        return f"Position(start={self.start}, end={self.end})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):
            return NotImplemented
        return (
            self.start == other.start
            and self.end == other.end
            and self._lineno == other._lineno
            and self._end_lineno == other._end_lineno
            and self._col_offset == other._col_offset
            and self._end_col_offset == other._end_col_offset
        )


@dataclass
class PartStatement:
    """Part of a statement with before/after components."""
    
    before: str = ""
    after: str = ""


@dataclass
class Statement:
    """Full statement with components."""
    
    top: PartStatement
    before: str
    self: str
    after: str

    @property
    def text(self) -> str:
        return f"{self.top.before}#{self.before}@{self.self}${self.after}{self.top.after}"

    def as_text(self, top_marker: str = "#", chain_marker: str = "$", current_marker: str = "@") -> str:
        return (
            f"{self.top.before}{top_marker}{self.before}"
            f"{current_marker}{self.self}{chain_marker}{self.after}{self.top.after}"
        )


class NestedAttributes:
    """Nested attribute access for leaf nodes."""
    
    def __init__(self, data: Dict[str, Any]) -> None:
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, NestedAttributes(value))
            else:
                setattr(self, key, value)


class Tree(Generic[T]):
    """Tree structure with position-aware nodes."""

    def __init__(
        self,
        source: T,
        start_lineno: Optional[int] = None,
        indent_size: int = 4,
    ) -> None:
        self.source = source
        self.start_lineno = start_lineno
        self.indent_size = indent_size
        self.root: Optional[Leaf] = None

    def add_leaf(self, leaf: "Leaf") -> None:
        if not self.root:
            self.root = leaf
            return

        if leaf.start is None or leaf.end is None:
            return

        best_match = self.root.find_best_match(leaf.start, leaf.end)
        if best_match:
            best_match.add_child(leaf)

    def find_best_match(self, start: int, end: int) -> Optional["Leaf"]:
        if self.root:
            return self.root.find_best_match(start, end)
        return None

    def flatten(self) -> List["Leaf"]:
        result: List["Leaf"] = []
        if self.root:
            result.append(self.root)
            for child in self.root.children:
                result.extend(self._flatten_helper(child))
        return result

    def _flatten_helper(self, leaf: "Leaf") -> List["Leaf"]:
        result = [leaf]
        for child in leaf.children:
            result.extend(self._flatten_helper(child))
        return result

    def to_json(self) -> str:
        return dumps(self._to_dict(), default=str)

    def _to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "start_lineno": self.start_lineno,
            "indent_size": self.indent_size,
            "root": self._node_to_dict(self.root) if self.root else None,
        }

    def _node_to_dict(self, node: Optional["Leaf"]) -> Optional[Dict[str, Any]]:
        if not node:
            return None
        return {
            "start": node.start,
            "end": node.end,
            "info": node.info,
            "children": [self._node_to_dict(child) for child in node.children],
            "style": node.style,
            "rich_style": node.rich_style,
        }

    @classmethod
    def from_json(cls, json_str: str) -> "Tree[T]":
        data = loads(json_str)
        tree = cls(data["source"], data["start_lineno"], data["indent_size"])
        if data["root"]:
            tree.root = cls._dict_to_node(data["root"])
        return tree

    @staticmethod
    def _dict_to_node(data: Dict[str, Any]) -> "Leaf":
        start = int(data["start"]) if data["start"] is not None else None
        end = int(data["end"]) if data["end"] is not None else None
        node = Leaf(
            start,
            data["info"],
            end,
            style=data.get("style"),
            rich_style=data.get("rich_style"),
        )
        for child_data in data["children"]:
            child = Tree._dict_to_node(child_data)
            node.add_child(child)
        return node

    def visualize(self, config: Optional["VisualizationConfig"] = None, root: Optional["Leaf"] = None) -> None:
        """Visualize tree structure."""
        from tree_interval.visualizer import TreeVisualizer
        TreeVisualizer.visualize(self, config, root)
