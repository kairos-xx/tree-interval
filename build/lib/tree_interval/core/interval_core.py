"""
Core tree data structures and position handling functionality.

This module provides foundational classes for managing tree structures with
interval-based positioning. It includes three main classes:

- Position: Handles position tracking with line numbers and column offsets
- Leaf: Represents nodes in the tree with position information
- Tree: Manages the overall tree structure and node relationships

Key Features:
    - Precise position tracking with line/column information
    - Parent-child relationship management
    - Tree traversal capabilities
    - JSON serialization support
    - Rich visualization

Technical Details:
    - Support for frame objects, tuples, or direct values
    - Bidirectional parent-child relationships
    - Generic typing for flexible data storage
    - Handles absolute and relative positions
"""

from dataclasses import dataclass
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
    NamedTuple,
    Optional,
    TypeVar,
    Union,
)

from .ast_types import AST_TYPES


class LeafStyle(NamedTuple):
    """Style configuration for leaf nodes.

    Attributes:
        color (str): Color in hex format (#RRGGBB) or named color
        bold (bool): Whether text should be bold, defaults to False
    """

    color: str
    bold: bool = False


@dataclass
class PartStatement:
    """Represents a statement part with before and after text"""

    before: str
    after: str


@dataclass
class Statement:
    """A complete breakdown of a code statement with marker annotations.

    This class provides functionality to represent and format code statements,
    particularly focusing on attribute chains and nested expressions.
    It supports customizable visual markers for different parts of
    the statement.

    The statement is broken down into several components:
    - Top-level statement parts (marked with '^' by default)
    - Chain/attribute parts (marked with '~' by default)
    - Current attribute/expression (marked with '*' by default)

    Each component can be formatted with different markers to visualize the
    structure of complex statements, especially useful for debugging and
    code analysis.

    Attributes:
        top (PartStatement): The top-level statement containing
            before/after parts
            Example: In 'print(obj.attr)', 'print(' is before, ')' is after
        before (str): Text before the current attribute/expression
            Example: In 'obj.attr1.attr2', 'obj.attr1.' is before
        self (str): The current attribute or expression text
            Example: In 'obj.attr1.attr2', if focused on 'attr1', that's self
        after (str): Text following the current attribute/expression
            Example: In 'obj.attr1.attr2', '.attr2' is after
        top_marker (str): Marker for top-level statement parts (default: '^')
        chain_marker (str): Marker for attribute chains (default: '~')
        current_marker (str): Marker for current attribute (default: '*')

    Example:
        >>> stmt = Statement(
        ...     top=PartStatement(before="print(", after=")"),
        ...     before="obj.", self="attr1", after=".attr2"
        ... )
        >>> print(stmt.as_text())
        print(obj.attr1.attr2)
        ^^^^^~~~~***~~~~~~^
    """

    top: PartStatement
    before: str
    self: str
    after: str
    top_marker: str = "~"
    chain_marker: str = "^"
    current_marker: str = "▲"

    def as_text(self,
                top_marker=None,
                chain_marker=None,
                current_marker=None) -> str:
        """Format the statement with visual marker annotations.

        Creates a two-line representation of the statement where the first line
        shows the actual code and the second line shows markers indicating the
        role of each part. The markers are aligned directly under their
        corresponding code parts.

        Args:
            top_marker (str, optional): Character for marking top-level parts.
                Defaults to self.top_marker if None.
            chain_marker (str, optional): Character for marking
                attribute chains.
                Defaults to self.chain_marker if None.
            current_marker (str, optional): Character for marking current
                attribute.
                Defaults to self.current_marker if None.

        Returns:
            str: A multi-line string with the code and aligned markers.
                Example:
                    print(obj.attr.value)
                    ^^^^^~~~~***~~~~~^
        """
        top_marker = top_marker or self.top_marker
        chain_marker = chain_marker or self.chain_marker
        current_marker = current_marker or self.current_marker

        def lines_with_markers(text: str, marker_char: str):
            return [
                (line,
                 "".join([ch if ch.isspace() else marker_char for ch in line]))
                for line in text.split("\n")
            ]

        def merge_lines(pairs_a, pairs_b):
            if not pairs_a:
                return pairs_b
            if not pairs_b:
                return pairs_a

            last_text_a, last_mark_a = pairs_a[-1]
            first_text_b, first_mark_b = pairs_b[0]
            return (pairs_a[:-1] + [
                (last_text_a + first_text_b, last_mark_a + first_mark_b)
            ] + pairs_b[1:])

        return "\n".join(
            sum(
                [[text_line, marker_line]
                 for text_line, marker_line in merge_lines(
                     merge_lines(
                         lines_with_markers(self.top.before, top_marker),
                         merge_lines(
                             merge_lines(
                                 lines_with_markers(self.before, chain_marker),
                                 lines_with_markers(self.self, current_marker),
                             ),
                             lines_with_markers(self.after, chain_marker),
                         ),
                     ),
                     lines_with_markers(self.top.after, top_marker),
                 )],
                [],
            ))

    @property
    def text(self) -> str:
        """Property access for default markers."""
        return self.as_text()


if TYPE_CHECKING:
    from ..visualizer.config import VisualizationConfig

T = TypeVar("T")


class Position:
    """
    Represents a position in source code with line and column tracking.

    Handles different types of position inputs and normalizes them into
    a consistent format with start/end positions and line/column info.

    Attributes:
        start (int): Starting position in the source
        end (int): Ending position in the source
        info (Any): Additional information about the position
        selected (bool): Whether this position is currently selected
        _lineno (int): Line number in source code
        _end_lineno (int): Ending line number
        _col_offset (int): Column offset from line start
        _end_col_offset (int): Ending column offset
        parent (Optional[Leaf]): Parent node in tree structure
        children (List[Leaf]): Child nodes in tree structure

    Implementation:
        - Handles frame objects for runtime tracking
        - Supports position objects from dis module
        - Maintains absolute and line-relative positions
        - Calculates indentation offsets
        - Preserves parent-child links
    """

    def __init__(
        self,
        start: Optional[Union[int, disposition, FrameType]] = None,
        end: Optional[int] = None,
        source: Optional[Union[str, dict]] = None,
        info: Optional[Any] = None,
        selected: bool = False,
    ):
        """
        Initialize a Position object.

        Args:
            start: Starting position, frame object, or disposition object
            end: Ending position
                (optional if start contains full position info)
            source: Source code string or metadata dictionary
            info: Additional position information
            selected: Selection state of this position

        Raises:
            ValueError: If both start and end are None for direct position init
        """
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
                    line_offset_val = (int(line_offset) if isinstance(
                        line_offset, int) else 0)
                    if (self._lineno is not None
                            and self._col_offset is not None and lines):
                        adjusted_lineno = (int(self._lineno) if isinstance(
                            self._lineno, int) else 1)
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
                self.start = (pos.col_offset if hasattr(pos, "col_offset")
                              and pos.col_offset is not None else 0)
                self.end = (pos.end_col_offset
                            if hasattr(pos, "end_col_offset")
                            and pos.end_col_offset is not None else 0)
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

                    pos_start = (
                        sum(len(line) + 1
                            for line in lines[:lineno - 1]) + col_offset)
                    pos_end = (
                        sum(len(line) + 1 for line in lines[:end_lineno - 1]) +
                        end_col_offset)
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
    def lineno(self) -> Optional[int]:
        """Get line number."""
        return self._lineno

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
            end_col_offset = (self.end_col_offset
                              if self.end_col_offset is not None else 0)
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
        if (self.position._end_col_offset is None
                and self.position._col_offset is not None):
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

    @property
    def is_set(self) -> bool:
        """Check if this node represents a set operation based on AST type."""
        if not self.info or not isinstance(self.info, dict):
            return False
        node_type = self.info.get("type")
        if not node_type:
            return False
        return AST_TYPES.get(node_type, {}).get("is_set", False)

    @property
    def statement(self) -> Statement:
        """Get statement information for this node using AST traversal."""
        top = self.top_statement
        if (self.parent and self.parent.ast_node is getattr(
                top.ast_node, "targets", [top.ast_node])[0] if top else None):
            top = None
        next_attr = self
        while True:
            next_attr_candidate = getattr(next_attr, "next_attribute", None)
            if next_attr_candidate is not None:
                next_attr = next_attr_candidate
            else:
                break

        # Handle current attribute
        value = getattr(self.ast_node, "cleaned_value", "")

        # Find remaining attributes in chain for 'after' part
        top_source = getattr(top, "info", {}).get("source", "")
        top_start = (top.end if top else 0) or 0
        top_part = PartStatement(
            before=top_source[:(self.start or 0) - top_start],
            after=top_source[((next_attr.end if next_attr else 0) or 0) -
                             top_start:],
        )
        source = self.info.get("source", "") if self.info else ""
        return Statement(
            top=top_part,
            before=source.removesuffix(value),
            self=value,
            after=getattr(next_attr, "info", {}).get("source",
                                                     "").removeprefix(source),
        )

    @property
    def next_attribute(self) -> Optional["Leaf"]:
        """Find the next attribute in a chained attribute access.
        Example: obj.attr1.attr2 -> for attr1 node, returns attr2 node
        Returns None if this is not part of an attribute chain or is
                the last attribute.
        """
        check = {"Attribute", "Name"}
        if not self.info or self.info.get("type") not in check:
            return None

        # If we're a Name node inside an attribute chain,
        # we shouldn't have a next
        if self.info.get("type") == "Name":
            return None

        current = self.parent
        while current:
            if current.info and current.info.get("type") in check:
                return current
            current = current.parent
        return None

    @property
    def previous_attribute(self) -> Optional["Leaf"]:
        """Find the previous attribute in a chained attribute access.
        Example: obj.attr1.attr2 -> for attr2 node, returns attr1 node"""
        check = {"Attribute", "Name"}
        if not self.info or self.info.get("type") not in check:
            return None

        # For attributes, look at children to find the previous one
        if self.children:
            for child in self.children:
                if child.info and child.info.get("type") in check:
                    return child

        return None

    @property
    def top_statement(self) -> Optional["Leaf"]:
        """
        Find the closest parent node that is a statement according
        to AST_TYPES.
        """
        current = self
        while current:
            if (current.info and isinstance(current.info, dict)
                    and current.info.get("type")
                    and current.info["type"] in AST_TYPES
                    and AST_TYPES[current.info["type"]]["statement"]):
                return current
            current = current.parent
        return None

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

        best_match_distance = (float("inf") if best_match_distance is None else
                               best_match_distance)
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
            return (f"Position(start={self.start}, end={self.end}, "
                    f"lineno={self.lineno}, end_lineno={self.end_lineno}, "
                    f"col_offset={self.col_offset}, " +
                    f"end_col_offset={self.end_col_offset}, "
                    f"size={self.size})")
        elif position_format == "tuple":
            return (
                f"({self.start}, {self.end}, {self.lineno}, "
                f"{self.end_lineno}, {self.col_offset}, {self.end_col_offset})"
            )
        else:
            return (f"Position(start={self.start}, " +
                    f"end={self.end}, size={self.size})")

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
            info_str = ("Info(" + ", ".join(f"{k}={repr(v)}"
                                            for k, v in self._info.items()) +
                        ")")
        else:
            info_str = repr(self._info)
        return f"Leaf(start={self.start}, end={self.end}, info={info_str})"

    def match(self, other: Any) -> bool:
        """Compare two nodes for equality."""
        if not isinstance(other, Leaf):
            return False
        return (self.position == other.position and self.info == other.info
                and self.start == other.start and self.end == other.end)


class Tree(Generic[T]):
    """
    A tree structure containing nodes with position information.

    Implements a generic tree where each node maintains position info and
    parent-child relationships. Supports JSON serialization and
    visualization.

    Type Parameters:
        T: Type of source data stored in the tree

    Attributes:
        source (T): Source data associated with the tree
        start_lineno (Optional[int]): Starting line number in source
        indent_size (int): Number of spaces per indentation level
        root (Optional[Leaf]): Root node of the tree

    Features:
        - Hierarchical node structure
        - Position-based node matching
        - Tree traversal methods
        - JSON serialization
        - Visualization support
    """

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
