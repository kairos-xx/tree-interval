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
    from tree_interval.core.leaf import Leaf


class IntervalCore:
    def __init__(self, root: "Leaf"):
        self.root = root

    def find_parent(self, criteria: Callable[["Leaf"], bool]) -> Optional["Leaf"]:
        """Finds the parent node matching the given criteria."""
        node = self.root
        while node is not None:
            if criteria(node):
                return node
            node = node.parent
        return None

    def find_child(self, criteria: Callable[["Leaf"], bool]) -> Optional["Leaf"]:
        """Finds the child node matching the given criteria."""
        if self.root is None:
            return None

        q = [self.root]
        while len(q) > 0:
            node = q.pop(0)
            if criteria(node):
                return node
            if node.children:
                q.extend(node.children)

        return None

    def find_sibling(self, criteria: Callable[["Leaf"], bool]) -> Optional["Leaf"]:
        """Finds the sibling node matching the given criteria."""
        if self.root is None or self.root.parent is None:
            return None

        for sibling in self.root.parent.children:
            if criteria(sibling) and sibling != self.root:
                return sibling
        return None

    def find_all_children(self, criteria: Callable[["Leaf"], bool]) -> List["Leaf"]:
        """Finds all children nodes matching the given criteria."""
        if self.root is None:
            return []

        results = []
        q = [self.root]
        while len(q) > 0:
            node = q.pop(0)
            if criteria(node):
                results.append(node)
            if node.children:
                q.extend(node.children)
        return results

    def find_all_parents(self, criteria: Callable[["Leaf"], bool]) -> List["Leaf"]:
        """Finds all parent nodes matching the given criteria."""
        if self.root is None:
            return []
        results = []
        node = self.root
        while node is not None:
            if criteria(node):
                results.append(node)
            node = node.parent
        return results

    def find_all_siblings(self, criteria: Callable[["Leaf"], bool]) -> List["Leaf"]:
        """Finds all sibling nodes matching the given criteria."""
        if self.root is None or self.root.parent is None:
            return []
        results = []
        for sibling in self.root.parent.children:
            if criteria(sibling) and sibling != self.root:
                results.append(sibling)
        return results

    # Other methods...
