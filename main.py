from typing import TypeVar, Optional, List, Generic, Iterator

T = TypeVar('T')  # Type variable for leaf information
L = TypeVar('L', bound='Leaf')  # Type variable for leaf instances


class Tree(Generic[T]):

    def __init__(self) -> None:
        self.root: Optional[Leaf[T]] = None

    def add_leaf(self, new_leaf: 'Leaf[T]') -> None:
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
        if not self.root:
            return None
        return self.root.find_best_match(target_start, target_end)

    def add_leaves(self, leaves: List['Leaf[T]']) -> None:
        if not leaves:
            return

        sorted_leaves = sorted(leaves,
                               key=lambda x: (-(x.end - x.start), x.start))
        self.root = sorted_leaves[0]
        for leaf in sorted_leaves[1:]:
            self.add_leaf(leaf)


class Leaf(tuple, Generic[T]):

    def __new__(cls,
                start: int,
                end: int,
                info: Optional[T] = None) -> 'Leaf[T]':
        if start > end:
            raise ValueError("Start must be less than or equal to end")
        instance = super().__new__(cls, (start, end))
        return instance

    def __init__(self, start: int, end: int, info: Optional[T] = None) -> None:
        self.info: Optional[T] = info
        self.children: List[Leaf[T]] = []
        self.parent: Optional[Leaf[T]] = None
        self.siblings: List[Leaf[T]] = []

    @property
    def start(self) -> int:
        return self[0]

    @property
    def end(self) -> int:
        return self[1]

    @classmethod
    def from_list(cls, leaves: List['Leaf[T]']) -> Optional['Leaf[T]']:
        if not leaves:
            return None

        sorted_leaves = sorted(leaves,
                               key=lambda x: (-(x.end - x.start), x.start))
        root = sorted_leaves[0]

        for leaf in sorted_leaves[1:]:
            current = root
            placed = False

            while not placed:
                if leaf.start == current.start and leaf.end == current.end:
                    current.add_sibling(leaf)
                    placed = True
                    continue

                if current.start <= leaf.start and leaf.end <= current.end:
                    child_placed = False
                    for child in current.children:
                        if child.start <= leaf.start and leaf.end <= child.end:
                            current = child
                            child_placed = True
                            break

                    if not child_placed:
                        current.add_child(leaf)
                        placed = True
                else:
                    raise ValueError(
                        f"Interval {leaf} cannot be placed in the tree")

        return root

    def add_child(self, child: 'Leaf[T]') -> None:
        if not isinstance(child, Leaf):
            raise TypeError("Child must be a Leaf instance")

        if child.start == self.start and child.end == self.end:
            self.add_sibling(child)
            return

        if not (self.start <= child.start and child.end <= self.end):
            raise ValueError(
                "Child interval must be contained within parent interval")

        children_to_move = [
            existing_child for existing_child in self.children
            if child.start <= existing_child.start
            and existing_child.end <= child.end
        ]

        for move_child in children_to_move:
            self.children.remove(move_child)
            child.children.append(move_child)
            move_child.parent = child

        child.parent = self
        self.children.append(child)

    def add_sibling(self, sibling: 'Leaf[T]') -> None:
        if not isinstance(sibling, Leaf):
            raise TypeError("Sibling must be a Leaf instance")
        if sibling.start != self.start or sibling.end != self.end:
            raise ValueError("Siblings must have the same interval")
        if sibling not in self.siblings:
            self.siblings.append(sibling)
            sibling.siblings.append(self)

    def find_best_match(self, target_start: int, target_end: int) -> 'Leaf[T]':

        def calculate_distance(leaf: 'Leaf[T]') -> int:
            start_diff = abs(leaf.start - target_start)
            end_diff = abs(leaf.end - target_end)
            return start_diff + end_diff

        best_leaf = self
        min_distance = calculate_distance(self)

        for child in self.children:
            if child.start <= target_start and child.end >= target_end:
                child_best = child.find_best_match(target_start, target_end)
                child_distance = calculate_distance(child_best)
                if child_distance < min_distance:
                    best_leaf = child_best
                    min_distance = child_distance

        return best_leaf

    def find_common_ancestor(self, other: 'Leaf[T]') -> Optional['Leaf[T]']:
        if not isinstance(other, Leaf):
            raise TypeError("Argument must be a Leaf instance")

        path1 = self._path_to_root()
        path2 = other._path_to_root()

        for node in path1:
            if node in path2:
                return node

        return None

    def _path_to_root(self) -> List['Leaf[T]']:
        path: List[Leaf[T]] = [self]
        current: Optional[Leaf[T]] = self
        while current and current.parent is not None:
            path.append(current.parent)
            current = current.parent
        return path

    def __repr__(self) -> str:
        return f"Leaf{super().__repr__()}, info={self.info})"

    def find_best_parent(self,
                         root: Optional['Leaf[T]']) -> Optional['Leaf[T]']:
        if not root:
            return None

        if root.start > self.start or root.end < self.end:
            return None

        best_parent = root
        for child in root.children:
            if child.start <= self.start and self.end <= child.end:
                potential_parent = self.find_best_parent(child)
                if potential_parent:
                    best_parent = potential_parent

        return best_parent


if __name__ == "__main__":
    # Example with string info
    leaf1: Leaf[str] = Leaf(1, 4, "First")
    leaf2: Leaf[str] = Leaf(2, 4, "Second")
    leaf3: Leaf[str] = Leaf(5, 8, "Third")
    root: Leaf[str] = Leaf(1, 10, "Root")

    tree: Tree[str] = Tree()
    tree.add_leaves([root, leaf1, leaf2, leaf3])

    best_match = root.find_best_match(2, 3)
    print(f"Best match for interval (2,3): {best_match}")
    print(f"Parent of best match: {best_match.parent}")
    print(f"Root's children: {root.children}")

    common = leaf1.find_common_ancestor(leaf2)
    print(f"Common ancestor of {leaf1} and {leaf2}: {common}")
