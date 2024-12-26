"""
Tree and Leaf implementation for interval-based hierarchical structures.

This module provides classes for creating and managing tree structures where nodes
represent intervals with typed information. It includes classes for handling positions,
tree nodes (leaves), and the main tree structure.

Classes:
    Position: Represents a position in source code with line/column information
    Leaf: A node in the tree structure with position and hierarchy information
    Tree: The main tree structure for managing hierarchical data
"""

# Standard library imports
from dataclasses import dataclass, field
from json import dumps, loads
from typing import TypeVar, Generic, List, Optional, NamedTuple, Any, Dict, Union

T = TypeVar('T')
L = TypeVar('L', bound='Leaf')


class Position(NamedTuple):
    """Represents a position in source code.
    
    Attributes:
        start: Starting absolute position
        end: Ending absolute position
        info: Additional information about the position
        lineno: Starting line number
        end_lineno: Ending line number
        col_offset: Starting column offset
        end_col_offset: Ending column offset
    """
    start: Optional[int] = None
    end: Optional[int] = None
    info: Optional[Any] = None
    lineno: Optional[int] = None
    end_lineno: Optional[int] = None
    col_offset: Optional[int] = None
    end_col_offset: Optional[int] = None

    @property
    def absolute_start(self) -> Optional[int]:
        return self.start if self.start is not None else None

    @property
    def absolute_end(self) -> Optional[int]:
        return self.end if self.end is not None else None


@dataclass
class Leaf(Generic[T]):
    _start: int
    _end: int
    info: Optional[T] = None
    children: List['Leaf[T]'] = field(default_factory=list)
    parent: Optional['Leaf[T]'] = None
    siblings: List['Leaf[T]'] = field(default_factory=list)
    lineno: Optional[int] = None
    end_lineno: Optional[int] = None
    col_offset: Optional[int] = None
    end_col_offset: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'start': self._start,
            'end': self._end,
            'info': self.info,
            'size': self.size,
            'children': [child.to_dict() for child in self.children],
            'complete': True
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Leaf[T]':
        leaf = cls(data['start'], data['end'], data['info'])
        if 'children' in data:
            for child_data in data['children']:
                child = cls.from_dict(child_data)
                leaf.add_child(child)
        return leaf

    def __repr__(self) -> str:
        return dumps(
            {
                'info': self.info,
                'start': self._start,
                'end': self._end,
                'children':
                [loads(child.__repr__()) for child in self.children]
            },
            indent=2)

    def __init__(self,
                 start_or_pos: Union[int, Position, tuple],
                 end: Optional[int] = None,
                 info: Optional[T] = None) -> None:
        self.children: List['Leaf[T]'] = []
        self.parent: Optional['Leaf[T]'] = None
        self.siblings: List['Leaf[T]'] = []
        self._start: int = 0
        self._end: int = 0

        if isinstance(start_or_pos, (Position, tuple)):
            pos = start_or_pos if isinstance(
                start_or_pos, Position) else Position(*start_or_pos)

            if pos.start is not None and pos.end is not None:
                self._start, self._end = pos.start, pos.end
            elif all(x is not None for x in [
                    pos.lineno, pos.end_lineno, pos.col_offset,
                    pos.end_col_offset
            ]):
                # Convert line/col to absolute positions
                assert pos.col_offset is not None
                assert pos.end_col_offset is not None
                self._start = pos.col_offset
                self._end = pos.end_col_offset
            else:
                raise ValueError(
                    "Either absolute positions or line/column positions must be provided"
                )

            self.info = pos.info
        else:
            self._start = start_or_pos
            self._end = end if end is not None else start_or_pos
            self.info = info

        if self._start > self._end:
            raise ValueError("Start must be less than or equal to end")

    @property
    def start(self) -> int:
        return self._start

    @property
    def end(self) -> int:
        return self._end

    @property
    def size(self) -> int:
        return self._end - self._start + 1

    def add_child(self, child: 'Leaf[T]') -> None:
        child.parent = self
        self.children.append(child)

    def find_best_parent(self, root: 'Leaf[T]') -> Optional['Leaf[T]']:
        if self._start >= root.start and self._end <= root.end:
            for child in root.children:
                result = self.find_best_parent(child)
                if result:
                    return result
            return root
        return None

    def find_best_match(self, target_start: int,
                        target_end: int) -> Optional['Leaf[T]']:
        if target_start >= self._start and target_end <= self._end:
            for child in self.children:
                match = child.find_best_match(target_start, target_end)
                if match:
                    return match
            return self
        return None

    def find_common_ancestor(self, other: 'Leaf[T]') -> Optional['Leaf[T]']:
        if not self.parent or not other.parent:
            return None
        if self.parent == other.parent:
            return self.parent
        return self.parent.find_common_ancestor(other.parent)

    def flatten(self) -> List['Leaf[T]']:
        result: List['Leaf[T]'] = [self]
        for child in self.children:
            result.extend(list(child.flatten()))
        return result

    def find_first_multi_child_ancestor(self) -> Optional['Leaf[T]']:
        current = self.parent
        while current:
            if len(current.children) > 1:
                return current
            current = current.parent
        return None


class Tree(Generic[T]):

    def __init__(self,
                 code: str,
                 start_lineno: int = 0,
                 indent_size: int = 0) -> None:
        self.root: Optional[Leaf[T]] = None
        self.code = code
        self.start_lineno = start_lineno
        self.indent_size = indent_size

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

    def to_json(self) -> str:
        data = {
            'code': self.code,
            'start_lineno': self.start_lineno,
            'indent_size': self.indent_size,
            'root': self.root.to_dict() if self.root else None,
            'complete': True
        }
        return dumps(data)

    @classmethod
    def from_json(cls, json_str: str) -> 'Tree[T]':
        data = loads(json_str)
        if not data.get('complete', False):
            raise ValueError("JSON data is not a complete tree serialization")

        tree = cls(code=data.get('code', ''),
                   start_lineno=data.get('start_lineno', 0),
                   indent_size=data.get('indent_size', 0))
        if data.get('root'):
            tree.root = Leaf.from_dict(data['root'])
        return tree

    def flatten(self) -> List['Leaf[T]']:
        if not self.root:
            return []
        return self.root.flatten()

    def visualize(self) -> None:
        if not self.root:
            print("Empty tree")
            return

        def _print_node(node: Leaf[T],
                        level: int = 0,
                        prefix: str = "") -> None:
            indent = "    " * level
            branch = "└── " if prefix == "└── " else "├── "
            print(
                f"{indent}{prefix}[{node.start}, {node.end}] (size={node.size})"
                + (f" info='{node.info}'" if node.info else ""))
            for i, child in enumerate(node.children):
                is_last = i == len(node.children) - 1
                _print_node(child, level + 1, "└── " if is_last else "├── ")

        _print_node(self.root)


def example_all_methods():
    """Demonstrate all available methods in Tree and Leaf classes."""
    print("1. Creating a tree and leaves")
    tree = Tree[str]("Example code", start_lineno=1, indent_size=4)

    # Create leaves with different methods
    root = Leaf(0, 100, "root")
    child1 = Leaf(Position(10, 40, "child1"))
    child2 = Leaf((50, 90, "child2"))  # Using tuple

    print("\n2. Building tree structure")
    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)

    # Create and add grandchildren
    grandchild1 = Leaf(15, 25, "grandchild1")
    grandchild2 = Leaf(60, 80, "grandchild2")
    child1.add_child(grandchild1)
    child2.add_child(grandchild2)

    print("\n3. Tree visualization")
    from tree_visualizer import TreeVisualizer, VisualizationConfig

    # Default visualization
    print("Default:")
    tree.visualize()

    # Custom visualizations
    print("\nWith Position objects:")
    TreeVisualizer.visualize(tree,
                             VisualizationConfig(position_format='position'))

    print("\nWith tuples and children count:")
    TreeVisualizer.visualize(
        tree,
        VisualizationConfig(position_format='tuple',
                            show_children_count=True,
                            show_size=False))

    print("\n4. Accessing properties")
    print(f"Root size: {root.size}")
    print(f"Child1 start: {child1.start}, end: {child1.end}")

    print("\n5. Finding nodes")
    best_match = tree.find_best_match(20, 30)
    print(f"Best match for (20, 30): {best_match}")

    common_ancestor = grandchild1.find_common_ancestor(grandchild2)
    print(f"Common ancestor of grandchildren: {common_ancestor}")

    multi_child = grandchild1.find_first_multi_child_ancestor()
    print(f"First multi-child ancestor: {multi_child}")

    print("\n6. Flattening tree")
    flat_list = tree.flatten()
    print("Flattened tree:", [leaf.info for leaf in flat_list])

    print("\n7. JSON serialization")
    json_str = tree.to_json()
    print("JSON string:", dumps(loads(json_str), indent=2))

    print("\n8. JSON deserialization")
    loaded_tree = Tree.from_json(json_str)
    print("Loaded tree:")
    loaded_tree.visualize()


if __name__ == "__main__":
    example_all_methods()


def example_ast_tree():
    """Example of using AstTreeBuilder"""
    import inspect
    from ast_tree_builder import AstTreeBuilder

    # Get current frame
    frame = inspect.currentframe()

    # Build AST tree
    builder = AstTreeBuilder(frame)
    ast_tree = builder.build()

    print("\nAST Tree visualization:")
    ast_tree.visualize()

    # Print flattened nodes
    print("\nFlattened AST nodes:")
    for leaf in ast_tree.flatten():
        print(f"{leaf.info}: [{leaf.start}, {leaf.end}]")


if __name__ == "__main__":
    example_all_methods()
    example_ast_tree()
