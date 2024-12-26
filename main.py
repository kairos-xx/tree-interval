"""
Tree and Leaf implementation for interval-based hierarchical structures.

This module provides classes for creating and managing tree structures where nodes
represent intervals with typed information.
"""

from typing import TypeVar, Optional, List, Generic, Iterator, NamedTuple, Union
import dis
from dataclasses import dataclass, field

# Type variables for generic type hints
T = TypeVar('T')  # Type variable for leaf information
L = TypeVar('L', bound='Leaf')  # Type variable for leaf instances


class Position(NamedTuple):
    start: int
    end: int
    info: Optional[any] = None


class Tree(Generic[T]):
    """A tree structure that manages interval-based Leaf nodes."""

    def __init__(self,
                 code: str,
                 start_lineno: int = 0,
                 indent_size: int = 0) -> None:
        """
        Initialize an empty tree with code parameters.
        
        Args:
            code: The source code string
            start_lineno: Base line number offset for all leaves
            indent_size: Base indentation size for all leaves
        """
        self.root: Optional[Leaf[T]] = None
        self.code = code
        self.start_lineno = start_lineno
        self.indent_size = indent_size

    def create_leaf(self,
                    position: dis.Positions,
                    info: Optional[T] = None) -> 'Leaf[T]':
        """
        Create a new leaf using tree's code parameters.
        
        Args:
            position: The dis.Positions object with position information
            info: Optional information for the leaf
            
        Returns:
            A new Leaf instance
        """
        return Leaf.from_position(position=position,
                                  code=self.code,
                                  start_lineno=self.start_lineno,
                                  indent_size=self.indent_size,
                                  info=info)

    def add_leaf(self, new_leaf: 'Leaf[T]') -> None:
        """
        Add a new leaf to the tree.

        Args:
            new_leaf: The leaf to be added to the tree.

        Raises:
            TypeError: If new_leaf is not a Leaf instance.
            ValueError: If no suitable parent is found.
        """
        if not isinstance(new_leaf, Leaf):
            raise TypeError("Must be a Leaf instance")

        if not self.root:
            self.root = new_leaf
            return

        best_parent = new_leaf.find_best_parent(self.root)
        if best_parent:
            best_parent.add_child(new_leaf)
        else:
            raise ValueError("Cannot find suitable parent for the new leaf")

    def find_best_match(self, target_start: int,
                        target_end: int) -> Optional['Leaf[T]']:
        """
        Find the leaf that best matches the target interval.

        Args:
            target_start: Start of target interval.
            target_end: End of target interval.

        Returns:
            The best matching leaf or None if tree is empty.
        """
        if not self.root:
            return None
        return self.root.find_best_match(target_start, target_end)

    def add_leaves(self, leaves: List['Leaf[T]']) -> None:
        """
        Add multiple leaves to the tree.

        Args:
            leaves: List of leaves to be added.
        """
        if not leaves:
            return

        # Sort leaves by size (descending) and start position
        sorted_leaves = sorted(leaves,
                               key=lambda x: (-(x.end - x.start), x.start))
        self.root = sorted_leaves[0]
        for leaf in sorted_leaves[1:]:
            self.add_leaf(leaf)

    def create_leaf_from_lines(self, start_line: int, end_line: int, info: Optional[T] = None) -> 'Leaf[T]':
        """
        Create a leaf from line numbers, automatically calculating positions and indentation.
        
        Args:
            start_line: Starting line number (1-based)
            end_line: Ending line number (1-based)
            info: Optional information for the leaf
            
        Returns:
            A new Leaf instance
        """
        lines = self.code.splitlines()
        if start_line < 1 or end_line > len(lines):
            raise ValueError("Line numbers out of range")
            
        # Get the block of code
        block_lines = lines[start_line-1:end_line]
        
        # Calculate indentation
        non_empty_lines = [l for l in block_lines if l.strip()]
        if non_empty_lines:
            indent_size = len(non_empty_lines[0]) - len(non_empty_lines[0].lstrip())
        else:
            indent_size = 0
            
        # Calculate start and end positions
        start_pos = sum(len(line) + 1 for line in lines[:start_line-1])
        end_pos = sum(len(line) + 1 for line in lines[:end_line-1]) + len(lines[end_line-1])
        
        # Create position object
        pos = Position(start_line, end_line, indent_size, end_pos - start_pos, info)
        
        return Leaf(pos)

    def visualize(self) -> None:
        """Print a visual representation of the tree structure."""
        if not self.root:
            print("Empty tree")
            return

        def _print_node(node: Leaf[T],
                        level: int = 0,
                        prefix: str = "") -> None:
            """Helper function to recursively print tree nodes."""
            indent = "    " * level
            branch = "└── " if prefix == "└── " else "├── "

            print(
                f"{indent}{prefix}[{node.start}, {node.end}] (size={node.size})"
                + (f" info='{node.info}'" if node.info else ""))

            for i, child in enumerate(node.children):
                is_last = i == len(node.children) - 1
                _print_node(child, level + 1, "└── " if is_last else "├── ")

        _print_node(self.root)


@dataclass
class Leaf(Generic[T]):
    """
    A leaf node representing an interval with typed information.
    Can be initialized from either a tuple/Position or individual values.
    """
    _start: int
    _end: int
    info: Optional[T] = None
    children: List['Leaf[T]'] = field(default_factory=list)
    parent: Optional['Leaf[T]'] = None
    siblings: List['Leaf[T]'] = field(default_factory=list)

    def __init__(self,
                 start_or_pos: Union[int, Position, tuple],
                 end: Optional[int] = None,
                 info: Optional[T] = None) -> None:
        if isinstance(start_or_pos, (Position, tuple)):
            pos = start_or_pos if isinstance(
                start_or_pos, Position) else Position(*start_or_pos)
            self._start, self._end, self.info = pos.start, pos.end, pos.info
        else:
            self._start = start_or_pos
            self._end = end
            self.info = info
            
        if self._start > self._end:
            raise ValueError("Start must be less than or equal to end")
            
        self.children = []
        self.parent = None
        self.siblings = []

    @property
    def start(self) -> int:
        """Get the start position of the interval."""
        return self._start

    @property
    def end(self) -> int:
        """Get the end position of the interval."""
        return self._end

    @property
    def size(self) -> int:
        """Get the size of the interval."""
        return self._end - self._start + 1

    def add_child(self, child: 'Leaf[T]') -> None:
        """Add a child to this leaf."""
        child.parent = self
        self.children.append(child)

    def find_best_parent(self, root: 'Leaf[T]') -> Optional['Leaf[T]']:
        """Find the best parent for this leaf in the tree."""
        if self._start >= root.start and self._end <= root.end:
            for child in root.children:
                result = self.find_best_parent(child)
                if result:
                    return result
            return root
        return None

    def find_best_match(self, target_start: int,
                        target_end: int) -> Optional['Leaf[T]']:
        """Find the best matching leaf for the given interval."""
        if target_start >= self._start and target_end <= self._end:
            for child in self.children:
                match = child.find_best_match(target_start, target_end)
                if match:
                    return match
            return self
        return None

    def find_common_ancestor(self, other: 'Leaf[T]') -> Optional['Leaf[T]']:
        """Find the common ancestor between this leaf and another."""
        if not self.parent or not other.parent:
            return None
        if self.parent == other.parent:
            return self.parent
        return self.parent.find_common_ancestor(other.parent)

    def find_first_multi_child_ancestor(self) -> Optional['Leaf[T]']:
        """
        Find the first ancestor that has more than one child.

        Returns:
            Optional[Leaf[T]]: The first ancestor with multiple children,
            or None if no such ancestor exists.
        """
        current = self.parent
        while current:
            if len(current.children) > 1:
                return current
            current = current.parent
        return None

    @classmethod
    def from_position(cls,
                      position: dis.Positions,
                      code: str,
                      start_lineno: int = 0,
                      indent_size: int = 0,
                      info: Optional[T] = None) -> 'Leaf[T]':
        """
        Create a Leaf from a dis.Position object.

        Args:
            position: The dis.Position object containing line and column information
            code: The multiline string of code
            start_lineno: Line number offset to be added to position's line numbers
            indent_size: Number of columns to add to position's column offsets
            info: Optional information to associate with the leaf

        Returns:
            A new Leaf instance representing the position in the code
        """
        # Calculate absolute line numbers
        abs_lineno = position.lineno + start_lineno
        abs_end_lineno = position.end_lineno + start_lineno if position.end_lineno else abs_lineno

        # Calculate absolute column positions
        abs_col_offset = position.col_offset + indent_size
        abs_end_col_offset = position.end_col_offset + indent_size if position.end_col_offset else abs_col_offset

        # Convert to absolute character position
        lines = code.splitlines()
        start_pos = sum(len(line) + 1
                        for line in lines[:abs_lineno - 1]) + abs_col_offset
        end_pos = sum(
            len(line) + 1
            for line in lines[:abs_end_lineno - 1]) + abs_end_col_offset

        return cls(start_pos, end_pos, info)


if __name__ == "__main__":
    # Example usage with code positions
    code = """def example():
    print("hello")
    return 42"""

    tree: Tree[str] = Tree(code, start_lineno=1, indent_size=4)

    # Create a position (simulated dis.Positions)
    class Position:
        def __init__(self, lineno, end_lineno, col_offset, end_col_offset, info=None):
            self.lineno = lineno
            self.end_lineno = end_lineno
            self.col_offset = col_offset
            self.end_col_offset = end_col_offset
            self.start = col_offset
            self.end = end_col_offset
            self.info = info

    # Calculate total code length for proper intervals
    total_length = len(code)

    # Create leaves using different representations
    root: Leaf[str] = Leaf(0, total_length, "Root")  # Using individual values
    leaf1: Leaf[str] = tree.create_leaf_from_lines(1, 1, "Function def")  # Create from line numbers
    leaf2: Leaf[str] = Leaf((13, 13, 0, 25, "Second"))  # Create from tuple (lineno, end_lineno, col_offset, end_col_offset, info)
    leaf3: Leaf[str] = Leaf(26, total_length,
                            "Third")  # Using individual values

    # Create and populate tree
    tree.add_leaves([root, leaf1, leaf2, leaf3])

    # Visualize the tree structure
    print("Tree visualization:")
    tree.visualize()

    # Demonstrate tree operations
    best_match = root.find_best_match(2, 3)
    print(f"\nBest match for interval (2,3): {best_match}")
    print(f"Parent of best match: {best_match.parent}")
    print(f"Root's children: {root.children}")

    common = leaf1.find_common_ancestor(leaf2)
    print(f"Common ancestor of {leaf1} and {leaf2}: {common}")

    # Test the new method
    multi_child_ancestor = leaf2.find_first_multi_child_ancestor()
    print(
        f"\nFirst ancestor with multiple children for leaf2: {multi_child_ancestor}"
    )
    if multi_child_ancestor:
        print(f"Number of children: {len(multi_child_ancestor.children)}")