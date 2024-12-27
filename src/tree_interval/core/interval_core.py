"""
Core tree data structures.

This module contains the core Tree and Leaf classes used across the project.
"""

from json import dumps, loads
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    TypeVar,
    Union,
)

if TYPE_CHECKING:
    from ..visualizer.config import VisualizationConfig

T = TypeVar("T")


class Position:
    def __init__(
        self,
        start: Optional[int] = None,
        end: Optional[int] = None,
        info: Optional[Any] = None,
    ):
        self.start = start
        self.end = end
        self.info = info
        self._lineno: Optional[int] = None
        self._end_lineno: Optional[int] = None
        self._col_offset: Optional[int] = None
        self._end_col_offset: Optional[int] = (
            end - start if start is not None and end is not None else 0
        )
        self.parent: Optional["Leaf"] = None
        self.children: List["Leaf"] = []

    @property
    def lineno(self) -> int:
        return self._lineno if self._lineno is not None else 1

    @lineno.setter
    def lineno(self, value: Optional[int]) -> None:
        self._lineno = value

    @property
    def end_lineno(self) -> int:
        return self._end_lineno if self._end_lineno is not None else 1

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

    def position_as(self, position_format: str = "default") -> str:
        """Display position with specific format."""
        if position_format == "position":
            col_offset = self.col_offset if self.col_offset is not None else 0
            end_col_offset = (
                self.end_col_offset if self.end_col_offset is not None else 0
            )
            return (
                f"Position(start={self.start}, "
                + f"end={self.end}, "
                + f"lineno={self.lineno}, "
                + f"end_lineno={self.end_lineno}, "
                + f"col_offset={col_offset}, "
                + f"end_col_offset={end_col_offset})"
            )
        elif position_format == "tuple":
            values = [
                self.start,
                self.end,
                self.lineno,
                self.end_lineno,
                self.col_offset if self.col_offset is not None else 0,
                self.end_col_offset if self.end_col_offset is not None else 0,
            ]
            return "(" + ", ".join(str(v) for v in values) + ")"
        else:
            return f"Position(start={self.start}, end={self.end})"

    def __str__(self) -> str:
        return f"Position(start={self.start}, end={self.end}, info={self.info})"

    def find_parent(self, criteria: Callable[["Leaf"], bool]) -> Optional["Leaf"]:
        """Find first parent that matches the criteria."""
        if not self.parent:
            return None
        if criteria(self.parent):
            return self.parent
        return self.parent.find_parent(criteria)

    def find_child(self, criteria: Callable[["Leaf"], bool]) -> Optional["Leaf"]:
        """Find first child that matches the criteria."""
        for child in self.children:
            if criteria(child):
                return child
            result = child.find_child(criteria)
            if result:
                return result
        return None

    def find_sibling(self, criteria: Callable[["Leaf"], bool]) -> Optional["Leaf"]:
        """Find first sibling that matches the criteria."""
        if not self.parent:
            return None
        for child in self.parent.children:
            if child != self and criteria(child):
                return child
        return None


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

        # Initialize end_col_offset if not set
        if (
            self.position._end_col_offset is None
            and self.position._col_offset is not None
        ):
            self.position._end_col_offset = self.position._col_offset + 20

        self.parent: Optional[Leaf] = None
        self.children: List[Leaf] = []
        self.ast_node: Optional[Any] = None
        self.attributes = NestedAttributes(self._as_dict())

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

    @property
    def lineno(self) -> Optional[int]:
        return self.position._lineno

    @property
    def end_lineno(self) -> Optional[int]:
        return self.position._end_lineno

    @property
    def col_offset(self) -> Optional[int]:
        return self.position._col_offset

    @property
    def end_col_offset(self) -> Optional[int]:
        return self.position._end_col_offset

    def add_child(self, child: "Leaf") -> None:
        """Add a child node to this leaf."""
        child.parent = self
        self.children.append(child)

    def find_best_match(self, start: int, end: int) -> Optional["Leaf"]:
        """Find the leaf that best matches the given range."""
        if self.start is None or self.end is None:
            return None

        if start >= self.start and end <= self.end:
            best_match = self
            for child in self.children:
                child_match = child.find_best_match(start, end)
                if (
                    child_match
                    and child_match.size
                    and best_match.size
                    and child_match.size < best_match.size
                ):
                    best_match = child_match
            return best_match
        return None

    def find_common_ancestor(self, other: "Leaf") -> Optional["Leaf"]:
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

    def find_first_multi_child_ancestor(self) -> Optional["Leaf"]:
        """Find the first ancestor that has multiple children."""
        current = self.parent
        while current:
            if len(current.children) > 1:
                return current
            current = current.parent
        return None

    def find_parent(self, criteria: Callable[["Leaf"], bool]) -> Optional["Leaf"]:
        """Find first parent node that matches the given criteria.

        Args:
            criteria: A function that takes a Leaf node and returns bool

        Returns:
            Matching parent node or None if not found
        """
        current = self.parent
        while current:
            if criteria(current):
                return current
            current = current.parent
        return None

    def find_child(self, criteria: Callable[["Leaf"], bool]) -> Optional["Leaf"]:
        """Find first child node that matches the given criteria.

        Args:
            criteria: A function that takes a Leaf node and returns bool

        Returns:
            Matching child node or None if not found
        """
        for child in self.children:
            if criteria(child):
                return child
            result = child.find_child(criteria)
            if result:
                return result
        return None

    def find_sibling(self, criteria: Callable[["Leaf"], bool]) -> Optional["Leaf"]:
        """Find first sibling node that matches the given criteria.

        Args:
            criteria: A function that takes a Leaf node and returns bool

        Returns:
            Matching sibling node or None if not found
        """
        if not self.parent:
            return None

        for sibling in self.parent.children:
            if sibling != self and criteria(sibling):
                return sibling
        return None

    def find(self, predicate: Callable[["Leaf"], bool]) -> Optional["Leaf"]:
        """Find first node matching predicate."""
        if predicate(self):
            return self
        parent_match = self.find_parent(predicate)
        if parent_match:
            return parent_match
        child_match = self.find_child(predicate)
        if child_match:
            return child_match
        sibling_match = self.find_sibling(predicate)
        if sibling_match:
            return sibling_match
        return None

    def _as_dict(self) -> Dict[str, Any]:
        """Return a dictionary containing all leaf information."""
        data = {
            "start": self.start,
            "end": self.end,
            "info": self.info,
            "size": self.size,
            "position": {
                "lineno": self.lineno,
                "end_lineno": self.end_lineno,
                "col_offset": self.col_offset,
                "end_col_offset": self.end_col_offset,
            },
            "children": [child._as_dict() for child in self.children],
        }
        self.attributes = NestedAttributes(data)
        return data

    def position_as(self, position_format: str = "default") -> str:
        """Display node with specific position format."""
        if position_format == "position":
            return (
                f"Position(start={self.start}, "
                + f"end={self.end}, "
                + f"lineno={self.lineno}, "
                + f"end_lineno={self.end_lineno}, "
                + f"col_offset={self.col_offset}, "
                + f"end_col_offset={self.end_col_offset}, "
                + f"size={self.size})"
            )
        elif position_format == "tuple":
            return (
                f"({self.start}, "
                + f"{self.end}, "
                + f"{self.lineno}, "
                + f"{self.end_lineno}, "
                + f"{self.col_offset}, "
                + f"{self.end_col_offset})"
            )
        else:
            return f"Position(start={self.start}, end={self.end}, size={self.size})"

    def __repr__(self) -> str:
        return f"Leaf(start={self.start}, end={self.end}, info={self.info})"


class Tree(Generic[T]):
    """A tree structure containing nodes with position information."""

    def __init__(
        self, source: T, start_lineno: Optional[int] = None, indent_size: int = 4
    ) -> None:
        self.source = source
        self.start_lineno = start_lineno
        self.indent_size = indent_size
        self.root: Optional[Leaf] = None

    def add_leaf(self, leaf: Leaf) -> None:
        """Add a leaf to the tree by finding its best matching parent."""
        if not self.root:
            self.root = leaf
            return

        if leaf.start is None or leaf.end is None:
            return

        best_match = self.root.find_best_match(leaf.start, leaf.end)
        if best_match:
            best_match.add_child(leaf)

    def find_best_match(self, start: int, end: int) -> Optional[Leaf]:
        """Find the leaf that best matches the given range."""
        if self.root:
            return self.root.find_best_match(start, end)
        return None

    def flatten(self) -> List[Leaf]:
        """Return a flattened list of all leaves in the tree."""
        result: List[Leaf] = []
        if self.root:
            result.append(self.root)
            for child in self.root.children:
                result.extend(self._flatten_helper(child))
        return result

    def _flatten_helper(self, leaf: Leaf) -> List[Leaf]:
        """Helper method for flatten()."""
        result = [leaf]
        for child in leaf.children:
            result.extend(self._flatten_helper(child))
        return result

    def to_json(self) -> str:
        """Convert the tree to a JSON string."""
        return dumps(self._to_dict())

    def _to_dict(self) -> Dict:
        """Convert the tree to a dictionary."""
        return {
            "source": self.source,
            "start_lineno": self.start_lineno,
            "indent_size": self.indent_size,
            "root": self._node_to_dict(self.root) if self.root else None,
        }

    def _node_to_dict(self, node: Optional[Leaf]) -> Optional[Dict]:
        """Convert a node to a dictionary."""
        if not node:
            return None
        return {
            "start": node.start,
            "end": node.end,
            "info": node.info,
            "children": [self._node_to_dict(child) for child in node.children],
        }

    @classmethod
    def from_json(cls, json_str: str) -> "Tree[T]":
        """Create a tree from a JSON string."""
        data = loads(json_str)
        tree = cls(data["source"], data["start_lineno"], data["indent_size"])
        if data["root"]:
            tree.root = cls._dict_to_node(data["root"])
        return tree

    @staticmethod
    def _dict_to_node(data: Dict) -> Leaf:
        """Create a node from a dictionary."""
        node = Leaf(data["start"], data["end"], data["info"])
        for child_data in data["children"]:
            child = Tree._dict_to_node(child_data)
            node.add_child(child)
        return node

    def visualize(self, config: Optional["VisualizationConfig"] = None) -> None:
        """Visualize the tree structure."""
        from ..visualizer import TreeVisualizer

        TreeVisualizer.visualize(self, config)


class NestedAttributes:
    position: "NestedAttributes"
    start: Optional[int]
    end: Optional[int]
    info: Any
    size: Optional[int]
    children: List[Dict[str, Any]]

    def __init__(self, data: Dict[str, Any]):
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, NestedAttributes(value))
            else:
                setattr(self, key, value)

    def __getattr__(self, name: str) -> Any:
        # Handle missing attributes gracefully
        return None

    def __repr__(self) -> str:
        attrs = [f"{k}={repr(v)}" for k, v in self.__dict__.items()]
        return f"NestedAttributes({', '.join(attrs)})"

    def __str__(self) -> str:
        return repr(self)
