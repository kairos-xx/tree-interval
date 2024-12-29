"""
Core tree data structures.

This module contains the core Tree and Leaf classes used across the project.
"""

from dis import Positions as disposition
from inspect import getframeinfo, getsource
from json import dumps, loads
from types import FrameType
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
        start: Optional[Union[int, disposition, FrameType]] = None,
        end: Optional[int] = None,
        source: Optional[Union[str, dict]] = None,
        info: Optional[Any] = None,
        selected: bool = False,
    ):
        self.info = info
        self.selected = selected
        self._lineno: Optional[int] = None
        self._end_lineno: Optional[int] = None
        self._col_offset: Optional[int] = None
        self._end_col_offset: Optional[int] = None
        if isinstance(start, FrameType):
            frame = start
            frame_info = getframeinfo(frame)
            common_indent = 0
            if source is None:
                try:
                    source = getsource(frame.f_code)
                    # Calculate indentation
                    lines = source.splitlines()
                    common_indent = min(
                        len(line) - len(line.lstrip()) for line in lines
                        if line.strip())
                    # Remove indentation and join
                    source = "\n".join(
                        line[common_indent:] if line.strip() else line
                        for line in lines)
                except (OSError, TypeError):
                    source = None
            pos = frame_info.positions if frame_info else None
            if pos and frame and frame.f_code:
                line_offset = (frame.f_code.co_firstlineno -
                               1 if frame.f_code.co_firstlineno else 0)
                self._lineno = pos.lineno if hasattr(pos, "lineno") else None
                self._end_lineno = (pos.end_lineno if hasattr(
                    pos, "end_lineno") else None)
                self._col_offset = (pos.col_offset if hasattr(
                    pos, "col_offset") else None)
                self._end_col_offset = (pos.end_col_offset if hasattr(
                    pos, "end_col_offset") else None)
                if source is not None and isinstance(source, str):
                    lines = source.split("\n")
                    line_offset_val = int(line_offset) if isinstance(
                        line_offset, int) else 0
                    if (self._lineno is not None
                            and self._col_offset is not None and lines):
                        adjusted_lineno = int(self._lineno) if isinstance(
                            self._lineno, int) else 1
                        line_idx = max(0,
                                       adjusted_lineno - line_offset_val - 1)
                        pos_start = (sum(
                            len(line) + 1 - common_indent
                            for line in lines[:line_idx]) if lines else 0)
                        pos_start = pos_start + (self._col_offset
                                                 if self._col_offset
                                                 is not None else 0)
                        if (self._end_lineno is not None
                                and self._end_col_offset is not None):
                            end_line_idx = max(
                                0,
                                (int(self._end_lineno) if isinstance(
                                    self._end_lineno, int) else 1) -
                                line_offset_val - 1,
                            )
                            pos_end = (sum(
                                len(line) + 1 - common_indent
                                for line in lines[:end_line_idx])
                                       if lines else pos_start)
                            pos_end = pos_end + (self._end_col_offset
                                                 if self._end_col_offset
                                                 is not None else 0)
                        else:
                            pos_end = pos_start
                        self.start = pos_start
                        self.end = pos_end

            elif pos and hasattr(pos, "col_offset") and hasattr(
                    pos, "end_col_offset"):
                self.start = pos.col_offset if hasattr(
                    pos, "col_offset") and pos.col_offset is not None else 0
                self.end = pos.end_col_offset if hasattr(
                    pos,
                    "end_col_offset") and pos.end_col_offset is not None else 0
            else:
                self.start = 0
                self.end = 0
        else:
            if isinstance(start, disposition):
                if isinstance(end, str):
                    source = end
                    end = None
                dis_pos = start
                pos_start = 0
                pos_end = 0
                if source is not None and isinstance(source, str):
                    # Calculate start and end from line/col offsets
                    lines = source.split("\n")
                    lineno = int(getattr(dis_pos, "lineno", 1))
                    end_lineno = int(getattr(dis_pos, "end_lineno", lineno))
                    col_offset = int(getattr(dis_pos, "col_offset", 0))
                    end_col_offset = int(
                        getattr(dis_pos, "end_col_offset", col_offset))

                    pos_start = sum(
                        len(line) + 1
                        for line in lines[:lineno - 1]) + col_offset
                    pos_end = sum(
                        len(line) + 1
                        for line in lines[:end_lineno - 1]) + end_col_offset
                    self.start = pos_start
                    self.end = pos_end
                else:
                    # Fallback to using line numbers as positions
                    # if no source provided
                    self.start = (dis_pos.col_offset
                                  if dis_pos.col_offset is not None else 0)
                    self.end = (dis_pos.end_col_offset
                                if dis_pos.end_col_offset is not None else 0)
            else:
                if start is None or end is None:
                    raise ValueError("Position start and end must not be None")
                self.start = start
                self.end = end

            if isinstance(end, int) and isinstance(start, int):
                self._end_col_offset: Optional[int] = (end or 0) - (start or 0)
        self.parent: Optional["Leaf"] = None
        self.children: List["Leaf"] = []

    @property
    def lineno(self) -> int:
        """Get line number with fallback to 1."""
        return self._lineno if self._lineno is not None else 1

    @lineno.setter
    def lineno(self, value: Optional[int]) -> None:
        """Set line number."""
        self._lineno = value

    @property
    def end_lineno(self) -> int:
        """Get end line number with fallback to 1."""
        return self._end_lineno if self._end_lineno is not None else 1

    @end_lineno.setter
    def end_lineno(self, value: Optional[int]) -> None:
        """Set end line number."""
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
            end_col_offset = (self.end_col_offset if self.end_col_offset is not None else 0)
            return (
                f"Position(start={self.start}, end={self.end}, "
                f"lineno={self.lineno}, end_lineno={self.end_lineno}, "
                f"col_offset={col_offset}, end_col_offset={end_col_offset})")
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
        return f"Position(start={self.start}, end={self.end})"

    def find_parent(self, criteria: Callable[["Leaf"],
                                             bool]) -> Optional["Leaf"]:
        """Find first parent that matches the criteria."""
        if not self.parent:
            return None
        if criteria(self.parent):
            return self.parent
        return self.parent.find_parent(criteria)

    def find_child(self, criteria: Callable[["Leaf"],
                                            bool]) -> Optional["Leaf"]:
        """Find first child that matches the criteria."""
        for child in self.children:
            if criteria(child):
                return child
            result = child.find_child(criteria)
            if result:
                return result
        return None

    def find_sibling(self, criteria: Callable[["Leaf"],
                                              bool]) -> Optional["Leaf"]:
        """Find first sibling that matches the criteria."""
        if not self.parent:
            return None
        for child in self.parent.children:
            if child != self and criteria(child):
                return child
        return None

    def __eq__(self, other: Any) -> bool:
        return self.start == other.start and self.end == other.end


class Leaf:
    """
    A node in the tree structure containing position
    and information data.
    """

    def __init__(
        self,
        position: Union[Position, tuple, int, None],
        info: Any = None,
        end: Optional[int] = None,
        style: Optional[Any] = None,
        rich_style: Optional[Any] = None,
    ):
        if position is None:
            position = Position(0, 0)

        if isinstance(position, Position):
            self.position = position
            self._info = info
        elif isinstance(position, tuple):
            self.position = Position(position[0], position[1])
            self._info = position[2] if len(position) > 2 else info
        else:
            self.position = Position(position, end)
            self._info = info

        self.style = style
        self.rich_style = rich_style

        # Initialize end_col_offset if not set
        if (self.position._end_col_offset is None and self.position._col_offset is not None):
            self.position._end_col_offset = self.position._col_offset + 20

        self.parent: Optional[Leaf] = None
        self.children: List[Leaf] = []
        self.ast_node: Optional[Any] = None
        self.attributes = NestedAttributes(self._as_dict())
        self.style = style
        self.rich_style = rich_style

    @property
    def start(self) -> Optional[int]:
        return self.position.start

    @property
    def end(self) -> Optional[int]:
        return self.position.end

    @property
    def info(self) -> Optional[Any]:
        return self._info

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

    @property
    def selected(self) -> bool:
        return self.position.selected

    @selected.setter
    def selected(self, value: bool) -> None:
        self.position.selected = value

    def add_child(self, child: "Leaf") -> None:
        """Add a child node to this leaf."""
        child.parent = self
        self.children.append(child)

    def find_best_match(
        self,
        start: int,
        end: int,
        best_match_distance: Optional[Union[int, float]] = None,
    ) -> Optional["Leaf"]:
        """Find the leaf that best matches the given range."""
        if self.start is None or self.end is None:
            return None

        def calc_distance(leaf: "Leaf") -> int:
            leaf_start = leaf.start or 0
            leaf_end = leaf.end or 0
            return ((start - leaf_start) if start > leaf_start else
                    (leaf_start - start)) + (
                        (end - leaf_end) if end > leaf_end else
                        (leaf_end - end))

        best_match_distance = float(
            "inf") if best_match_distance is None else best_match_distance
        distance = calc_distance(self)
        if distance < best_match_distance:
            best_match_distance = distance
        best_match = self
        for child in self.children:
            child_match = child.find_best_match(start, end,
                                                best_match_distance)
            if child_match is not None:
                distance = calc_distance(child_match)
                if distance < best_match_distance:
                    best_match_distance = distance
                    best_match = child_match
        return best_match

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

    def find_parent(self, criteria: Callable[["Leaf"],
                                             bool]) -> Optional["Leaf"]:
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

    def find_child(self, criteria: Callable[["Leaf"],
                                            bool]) -> Optional["Leaf"]:
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

    def find_sibling(self, criteria: Callable[["Leaf"],
                                              bool]) -> Optional["Leaf"]:
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
            "info": self._info,
            "size": self.size,
            "position": {
                "lineno": self.lineno,
                "end_lineno": self.end_lineno,
                "col_offset": self.col_offset,
                "end_col_offset": self.end_col_offset,
            },
            "children": [child._as_dict() for child in self.children],
            "style": self.style,
            "rich_style": self.rich_style,
        }
        self.attributes = NestedAttributes(data)
        return data

    def position_as(self, position_format: str = "default") -> str:
        """Display node with specific position format."""
        if position_format == "position":
            return (
                f"Position(start={self.start}, end={self.end}, "
                f"lineno={self.lineno}, end_lineno={self.end_lineno}, "
                f"col_offset={self.col_offset}, "+f"end_col_offset={self.end_col_offset}, "
                f"size={self.size})")
        elif position_format == "tuple":
            return (
                f"({self.start}, {self.end}, {self.lineno}, "
                f"{self.end_lineno}, {self.col_offset}, {self.end_col_offset})"
            )
        else:
            return (f"Position(start={self.start}, end={self.end}, size={self.size})")

    def _get_parent(self) -> Optional["Leaf"]:
        """Safe accessor for parent property."""
        return self.parent if self.parent is not None else None

    @property
    def next(self) -> Optional["Leaf"]:
        """Get the next leaf node in the tree traversal order."""
        parent = self._get_parent()
        if parent is None:
            return None

        siblings = parent.children
        try:
            idx = siblings.index(self)
            if idx < len(siblings) - 1:
                return siblings[idx + 1]
            # If last sibling, get first child of next parent
            next_parent = parent.next
            if next_parent is not None and next_parent.children:
                return next_parent.children[0]
        except ValueError:
            pass
        return None

    @property
    def previous(self) -> Optional["Leaf"]:
        """Get the previous leaf node in the tree traversal order."""
        parent = self._get_parent()
        if parent is None:
            return None

        siblings = parent.children
        try:
            idx = siblings.index(self)
            if idx > 0:
                return siblings[idx - 1]
            # If first sibling, get last child of previous parent
            prev_parent = parent.previous
            if prev_parent is not None and prev_parent.children:
                return prev_parent.children[-1]
        except ValueError:
            pass
        return None

    def get_ancestors(self) -> List["Leaf"]:
        """Get all ancestor nodes of this leaf."""
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors

    def __repr__(self) -> str:
        if isinstance(self._info, dict):
            info_str = "Info(" + ", ".join(
                f"{k}={repr(v)}" for k, v in self._info.items()) + ")"
        else:
            info_str = repr(self._info)
        return f"Leaf(start={self.start}, end={self.end}, info={info_str})"

    def match(self, other: Any) -> bool:
        """Compare two nodes for equality."""
        if not isinstance(other, Leaf):
            return False
        return self.position == other.position and self.info == other.info and self.start == other.start and self.end == other.end


class Tree(Generic[T]):
    """A tree structure containing nodes with position information."""

    def __init__(self,
                 source: T,
                 start_lineno: Optional[int] = None,
                 indent_size: int = 4) -> None:
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
            "info": node._info,
            "children": [self._node_to_dict(child) for child in node.children],
            "style": node.style,
            "rich_style": node.rich_style,
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
        start = int(data["start"]) if data["start"] is not None else None
        end = int(data["end"]) if data["end"] is not None else None
        node = Leaf(start,
                    data["info"],
                    end,
                    style=data.get("style"),
                    rich_style=data.get("rich_style"))
        for child_data in data["children"]:
            child = Tree._dict_to_node(child_data)
            node.add_child(child)
        return node

    def visualize(self,
                  config: Optional["VisualizationConfig"] = None) -> None:
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
    style: Optional[Any]
    rich_style: Optional[Any]

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
