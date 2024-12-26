
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

    def visualize(self) -> None:
        """Print a visual representation of the tree structure."""
        if not self.root:
            print("Empty tree")
            return

        def _print_node(node: Leaf[T], level: int = 0, prefix: str = "") -> None:
            """Helper function to recursively print tree nodes."""
            indent = "    " * level
            branch = "└── " if prefix == "└── " else "├── "
            
            print(f"{indent}{prefix}[{node.start}, {node.end}]" + 
                  (f" ({node.info})" if node.info else ""))
            
            for i, child in enumerate(node.children):
                is_last = i == len(node.children) - 1
                _print_node(child, level + 1, "└── " if is_last else "├── ")

        _print_node(self.root)


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

    def add_child(self, child: 'Leaf[T]') -> None:
        """Add a child to this leaf."""
        child.parent = self
        self.children.append(child)

    def find_best_parent(self, root: 'Leaf[T]') -> Optional['Leaf[T]']:
        """Find the best parent for this leaf in the tree."""
        if self.start >= root.start and self.end <= root.end:
            for child in root.children:
                result = self.find_best_parent(child)
                if result:
                    return result
            return root
        return None

    def find_best_match(self, target_start: int,
                       target_end: int) -> Optional['Leaf[T]']:
        """Find the best matching leaf for the given interval."""
        if target_start >= self.start and target_end <= self.end:
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


if __name__ == "__main__":
    # Example usage with string information
    leaf1: Leaf[str] = Leaf(1, 4, "First")
    leaf2: Leaf[str] = Leaf(2, 4, "Second")
    leaf3: Leaf[str] = Leaf(5, 8, "Third")
    root: Leaf[str] = Leaf(1, 10, "Root")

    # Create and populate tree
    tree: Tree[str] = Tree()
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
