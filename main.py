
"""
Tree and Leaf implementation for interval-based hierarchical structures.

This module provides classes for creating and managing tree structures where nodes
represent intervals with typed information.
"""

from typing import TypeVar, Optional, List, Generic, Iterator

# Type variables for generic type hints
T = TypeVar('T')  # Type variable for leaf information
L = TypeVar('L', bound='Leaf')  # Type variable for leaf instances


class Tree(Generic[T]):
    """A tree structure that manages interval-based Leaf nodes."""

    def __init__(self) -> None:
        """Initialize an empty tree."""
        self.root: Optional[Leaf[T]] = None

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


class Leaf(tuple, Generic[T]):
    """
    A leaf node representing an interval with typed information.

    Inherits from tuple to make it immutable and hashable.
    """

    def __new__(cls, start: int, end: int,
                info: Optional[T] = None) -> 'Leaf[T]':
        """Create a new Leaf instance."""
        if start > end:
            raise ValueError("Start must be less than or equal to end")
        instance = super().__new__(cls, (start, end))
        return instance

    def __init__(self, start: int, end: int, info: Optional[T] = None) -> None:
        """
        Initialize a Leaf instance.

        Args:
            start: Start of interval.
            end: End of interval.
            info: Optional information associated with the leaf.
        """
        self.info: Optional[T] = info
        self.children: List[Leaf[T]] = []
        self.parent: Optional[Leaf[T]] = None
        self.siblings: List[Leaf[T]] = []

    @property
    def start(self) -> int:
        """Get the start position of the interval."""
        return self[0]

    @property
    def end(self) -> int:
        """Get the end position of the interval."""
        return self[1]

[... remaining methods with similar docstring formatting ...]

if __name__ == "__main__":
    # Example usage with string information
    leaf1: Leaf[str] = Leaf(1, 4, "First")
    leaf2: Leaf[str] = Leaf(2, 4, "Second")
    leaf3: Leaf[str] = Leaf(5, 8, "Third")
    root: Leaf[str] = Leaf(1, 10, "Root")

    # Create and populate tree
    tree: Tree[str] = Tree()
    tree.add_leaves([root, leaf1, leaf2, leaf3])

    # Demonstrate tree operations
    best_match = root.find_best_match(2, 3)
    print(f"Best match for interval (2,3): {best_match}")
    print(f"Parent of best match: {best_match.parent}")
    print(f"Root's children: {root.children}")

    common = leaf1.find_common_ancestor(leaf2)
    print(f"Common ancestor of {leaf1} and {leaf2}: {common}")
