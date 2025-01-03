
"""Complete Tree Interval Implementation."""

from dataclasses import dataclass
from inspect import currentframe, FrameType, stack
from rich.console import Console
from rich.style import Style
from rich.tree import Tree as RichTree
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
import ast
import json
import sys

T = TypeVar('T')

@dataclass
class Position:
    """Position with line and column information."""
    start: Optional[int]
    end: Optional[int]
    selected: bool = False

    def __post_init__(self) -> None:
        self._lineno: Optional[int] = None
        self._end_lineno: Optional[int] = None
        self._col_offset: Optional[int] = None
        self._end_col_offset: Optional[int] = None

    @property
    def lineno(self) -> Optional[int]:
        return self._lineno

    @lineno.setter
    def lineno(self, value: Optional[int]) -> None:
        self._lineno = value

    @property
    def end_lineno(self) -> Optional[int]:
        return self._end_lineno

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

@dataclass
class LeafStyle:
    """Style configuration for tree nodes."""
    color: str
    bold: bool = False

@dataclass 
class VisualizationConfig:
    """Configuration for tree visualization."""
    show_info: bool = True
    show_size: bool = True
    show_children_count: bool = False
    position_format: str = "default"
    root_style: Optional[Style] = None
    node_style: Optional[Style] = None
    leaf_style: Optional[Style] = None

class Tree(Generic[T]):
    """Tree structure with position-aware nodes."""

    def __init__(self, source: T) -> None:
        self.source = source
        self.root: Optional['Leaf'] = None

    def add_leaf(self, leaf: 'Leaf') -> None:
        """Add a leaf to the tree."""
        if not self.root:
            self.root = leaf
            return
        
        if leaf.start is None or leaf.end is None:
            return

        best_match = self.root.find_best_match(leaf.start, leaf.end)
        if best_match:
            best_match.add_child(leaf)

    def find_best_match(self, start: int, end: int) -> Optional['Leaf']:
        """Find best matching node for position."""
        if not self.root:
            return None
        return self.root.find_best_match(start, end)

    def visualize(self, config: Optional[VisualizationConfig] = None, root: Optional['Leaf'] = None) -> None:
        """Visualize tree structure."""
        TreeVisualizer.visualize(self, config, root)

    def flatten(self) -> List['Leaf']:
        """Get flattened list of all nodes."""
        if not self.root:
            return []
        return self.root.flatten()

    def to_json(self) -> str:
        """Convert tree to JSON."""
        if not self.root:
            return "{}"
        return json.dumps(self.root._as_dict())

    @classmethod
    def from_json(cls, json_str: str) -> 'Tree':
        """Create tree from JSON."""
        data = json.loads(json_str)
        tree = cls("")
        if data:
            tree.root = Leaf.from_dict(data)
        return tree

class Leaf:
    """Node in tree structure."""

    def __init__(
        self,
        position: Union[Position, tuple, int],
        info: Any = None,
        end: Optional[int] = None,
    ) -> None:
        if isinstance(position, Position):
            self.position = position
        elif isinstance(position, tuple):
            self.position = Position(position[0], position[1])
        else:
            self.position = Position(position, end)

        self.info = info
        self.parent: Optional[Leaf] = None
        self.children: List[Leaf] = []
        self.style: Optional[LeafStyle] = None
        self.rich_style: Optional[Style] = None
        self.selected: bool = False

    @property
    def start(self) -> Optional[int]:
        return self.position.start

    @property
    def end(self) -> Optional[int]:
        return self.position.end

    @property
    def size(self) -> int:
        return (self.end or 0) - (self.start or 0)

    def add_child(self, child: 'Leaf') -> None:
        """Add child node."""
        child.parent = self
        self.children.append(child)

    def find_best_match(
        self,
        start: int,
        end: int,
        best_match_distance: Optional[float] = None
    ) -> Optional['Leaf']:
        """Find best matching node for range."""
        if self.start is None or self.end is None:
            return None

        if best_match_distance is None:
            best_match_distance = float('inf')

        current_distance = abs(start - self.start) + abs(end - self.end)
        best_match = self if current_distance < best_match_distance else None

        for child in self.children:
            child_match = child.find_best_match(start, end, current_distance)
            if child_match:
                best_match = child_match

        return best_match

    def flatten(self) -> List['Leaf']:
        """Get flattened list of all nodes."""
        result = [self]
        for child in self.children:
            result.extend(child.flatten())
        return result

    def _as_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary."""
        return {
            'position': {
                'start': self.start,
                'end': self.end,
                'lineno': self.position.lineno,
                'end_lineno': self.position.end_lineno,
                'col_offset': self.position.col_offset,
                'end_col_offset': self.position.end_col_offset,
                'selected': self.position.selected
            },
            'info': self.info,
            'children': [child._as_dict() for child in self.children]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Leaf':
        """Create node from dictionary."""
        pos = Position(data['position']['start'], data['position']['end'])
        pos.lineno = data['position']['lineno']
        pos.end_lineno = data['position']['end_lineno']
        pos.col_offset = data['position']['col_offset']
        pos.end_col_offset = data['position']['end_col_offset']
        pos.selected = data['position']['selected']

        leaf = cls(pos, data['info'])
        for child_data in data['children']:
            child = cls.from_dict(child_data)
            leaf.add_child(child)
        return leaf

class TreeVisualizer:
    """Tree visualization."""

    @staticmethod
    def visualize(tree: Tree, config: Optional[VisualizationConfig] = None, root: Optional[Leaf] = None) -> None:
        """Visualize tree structure."""
        if not config:
            config = VisualizationConfig()

        if not tree.root:
            return

        console = Console()
        rich_tree = RichTree(f"[bold]{tree.source}[/bold]")
        
        start_node = root if root else tree.root
        TreeVisualizer._build_rich_tree(start_node, rich_tree, config)
        
        console.print(rich_tree)

    @staticmethod
    def _build_rich_tree(node: Leaf, rich_tree: RichTree, config: VisualizationConfig) -> None:
        """Build rich tree recursively."""
        for child in node.children:
            label_parts = []
            
            if config.show_info and hasattr(child, 'info'):
                label_parts.append(str(child.info))
            
            if config.show_size:
                label_parts.append(f"({child.size})")
            
            if config.show_children_count:
                label_parts.append(f"[{len(child.children)}]")
            
            label = " ".join(label_parts)
            
            style = child.rich_style if hasattr(child, 'rich_style') else None
            branch = rich_tree.add(label, style=style)
            
            TreeVisualizer._build_rich_tree(child, branch, config)

class Future:
    """Dynamic attribute handling."""
    
    def __new__(
        cls,
        name: str,
        instance: object,
        frame: Optional[Union[int, FrameType]] = None,
        new_return: Optional[Any] = None,
    ) -> Any:
        """Handle dynamic attribute access."""
        if isinstance(frame, int):
            frame = sys._getframe(frame)
        elif frame is None:
            frame = currentframe()

        if frame is None:
            return new_return if new_return is not None else None

        return getattr(instance, name, new_return)

def create_example_tree() -> Tree:
    """Create example tree structure."""
    tree = Tree("Example")
    root = Leaf(Position(0, 100), info="Root")
    child1 = Leaf(Position(10, 40), info="Child 1")
    child2 = Leaf(Position(50, 90), info="Child 2")
    grandchild = Leaf(Position(15, 35), info="Grandchild")

    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)
    child1.add_child(grandchild)

    return tree

if __name__ == "__main__":
    # Example usage
    tree = create_example_tree()
    tree.visualize()
