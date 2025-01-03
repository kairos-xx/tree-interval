
"""Complete Tree Interval Implementation with all core components."""

from dataclasses import dataclass
from inspect import currentframe, FrameType, getsource, stack, getframeinfo
from rich.console import Console
from rich.style import Style
from rich.tree import Tree as RichTree
from textwrap import dedent, indent
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, Union
import ast
import json
import sys
from types import FrameType

T = TypeVar('T')

# AST Types mapping
AST_TYPES = {
    "Module": {"description": "Root node for entire file", "statement": True, "is_set": False},
    "Import": {"description": "Import statement", "statement": True, "is_set": False},
    "ImportFrom": {"description": "From import statement", "statement": True, "is_set": False},
    "FunctionDef": {"description": "Function definition", "statement": True, "is_set": False},
    "ClassDef": {"description": "Class definition", "statement": True, "is_set": False},
    "Assign": {"description": "Assignment operation", "statement": True, "is_set": True},
    "Name": {"description": "Variable or function name", "statement": False, "is_set": False},
    "Attribute": {"description": "Attribute access", "statement": False, "is_set": False},
}

@dataclass
class LeafStyle:
    """Style configuration for leaf nodes."""
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

@dataclass
class PartStatement:
    """Represents a statement part with before and after text."""
    before: str
    after: str

@dataclass
class Statement:
    """Complete breakdown of a code statement."""
    top: PartStatement
    before: str
    self: str
    after: str
    top_marker: str = "~"
    chain_marker: str = "^"
    current_marker: str = "▲"

    def as_text(self, top_marker=None, chain_marker=None, current_marker=None) -> str:
        top_marker = top_marker or self.top_marker
        chain_marker = chain_marker or self.chain_marker
        current_marker = current_marker or self.current_marker
        
        text = (self.top.before + self.before + self.self + 
               self.after + self.top.after)
        markers = (len(self.top.before) * top_marker + 
                  len(self.before) * chain_marker +
                  len(self.self) * current_marker + 
                  len(self.after) * chain_marker +
                  len(self.top.after) * top_marker)
        return f"{text}\n{markers}"

    @property
    def text(self) -> str:
        return self.as_text()

class Position:
    """Represents a code position with line/column tracking."""
    
    def __init__(
        self,
        start: Optional[Union[int, FrameType]] = None,
        end: Optional[int] = None,
        source: Optional[str] = None,
        info: Optional[Any] = None,
        selected: bool = False
    ):
        self.start = start if isinstance(start, (int, type(None))) else 0
        self.end = end
        self.info = info
        self.selected = selected
        self._lineno: Optional[int] = None
        self._end_lineno: Optional[int] = None
        self._col_offset: Optional[int] = None
        self._end_col_offset: Optional[int] = None
        
        if isinstance(start, FrameType):
            frame = start
            source = getsource(frame)
            frame_info = getframeinfo(frame)
            if frame_info.positions:
                self._lineno = frame_info.positions.lineno
                self._end_lineno = frame_info.positions.end_lineno
                self._col_offset = frame_info.positions.col_offset
                self._end_col_offset = frame_info.positions.end_col_offset
                
        self.parent: Optional['Leaf'] = None
        self.children: List['Leaf'] = []

    def position_as(self, position_format: str = "default") -> str:
        if position_format == "position":
            return (f"Position(start={self.start}, end={self.end}, "
                   f"lineno={self._lineno}, end_lineno={self._end_lineno}, "
                   f"col_offset={self._col_offset}, "
                   f"end_col_offset={self._end_col_offset})")
        elif position_format == "tuple":
            return f"({self.start}, {self.end})"
        return f"Position(start={self.start}, end={self.end})"

class Leaf:
    """A node in the tree structure containing position and information data."""
    
    def __init__(
        self,
        position: Union[Position, tuple, int, None],
        info: Any = None,
        end: Optional[int] = None,
        style: Optional[LeafStyle] = None,
        rich_style: Optional[Style] = None,
    ):
        if isinstance(position, Position):
            self.position = position
        elif isinstance(position, tuple):
            self.position = Position(position[0], position[1])
            info = position[2] if len(position) > 2 else info
        else:
            self.position = Position(position, end)
            
        self._info = info
        self.style = style
        self.rich_style = rich_style
        self.parent: Optional[Leaf] = None
        self.children: List[Leaf] = []
        self.ast_node: Optional[Any] = None

    @property
    def info(self) -> Any:
        return self._info

    @property
    def start(self) -> Optional[int]:
        return self.position.start

    @property
    def end(self) -> Optional[int]:
        return self.position.end

    @property
    def size(self) -> Optional[int]:
        if self.start is None or self.end is None:
            return None
        return self.end - self.start

    def add_child(self, child: 'Leaf') -> None:
        child.parent = self
        self.children.append(child)

    def find_best_match(self, start: int, end: int) -> Optional['Leaf']:
        if self.start is None or self.end is None:
            return None

        def calc_distance(leaf: 'Leaf') -> int:
            leaf_start = leaf.start or 0
            leaf_end = leaf.end or 0
            return abs(start - leaf_start) + abs(end - leaf_end)

        best_match = self
        best_distance = calc_distance(self)

        for child in self.children:
            child_match = child.find_best_match(start, end)
            if child_match:
                child_distance = calc_distance(child_match)
                if child_distance < best_distance:
                    best_match = child_match
                    best_distance = child_distance

        return best_match

class Tree(Generic[T]):
    """Generic tree structure for position-aware hierarchical data."""
    
    def __init__(self, source: T):
        self.source = source
        self.root: Optional[Leaf] = None

    def add_leaf(self, leaf: Leaf) -> None:
        if not self.root:
            self.root = leaf
            return

        if leaf.start is None or leaf.end is None:
            return

        best_match = self.root.find_best_match(leaf.start, leaf.end)
        if best_match:
            best_match.add_child(leaf)

    def find_best_match(self, start: int, end: int) -> Optional[Leaf]:
        if self.root:
            return self.root.find_best_match(start, end)
        return None

    def flatten(self) -> List[Leaf]:
        result: List[Leaf] = []
        if self.root:
            result.append(self.root)
            for child in self.root.children:
                result.extend(self._flatten_helper(child))
        return result

    def _flatten_helper(self, leaf: Leaf) -> List[Leaf]:
        result = [leaf]
        for child in leaf.children:
            result.extend(self._flatten_helper(child))
        return result

    def to_json(self) -> str:
        return json.dumps(self._to_dict(), default=str)

    def _to_dict(self) -> Dict:
        return {
            "source": self.source,
            "root": self._node_to_dict(self.root) if self.root else None,
        }

    def _node_to_dict(self, node: Optional[Leaf]) -> Optional[Dict]:
        if not node:
            return None
        return {
            "start": node.start,
            "end": node.end,
            "info": node._info,
            "children": [self._node_to_dict(child) for child in node.children],
        }

    def visualize(self, config: Optional[VisualizationConfig] = None) -> None:
        if not config:
            config = VisualizationConfig()

        if not self.root:
            return

        console = Console()
        rich_tree = RichTree(f"[bold]{self.source}[/bold]")
        self._build_rich_tree(self.root, rich_tree, config)
        console.print(rich_tree)

    def _build_rich_tree(self, node: Leaf, rich_tree: RichTree, 
                        config: VisualizationConfig) -> None:
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
            self._build_rich_tree(child, branch, config)

class Future:
    """Handles dynamic attribute creation and access."""
    
    def __new__(
        cls,
        name: str,
        instance: object,
        frame: Optional[Union[int, FrameType]] = None,
        new_return: Optional[Any] = None,
    ) -> Any:
        if not isinstance(frame, FrameType):
            frame = stack()[frame + 1 if isinstance(frame, int) else 2].frame

        sys.tracebacklimit = 0
        header = f"Attribute {name} not found"
        footer = indent(
            f'File "{frame.f_code.co_filename}" '
            f"line {frame.f_lineno}, in {frame.f_code.co_name}",
            "   ",
        )

        new = AttributeError(f"{header}\n{footer}")
        
        # Create and set new attribute if in setting context
        new = type(instance)() if new_return is None else new_return
        setattr(instance, name, new)
        return new

class AstTreeBuilder:
    """Builds tree structures from Python Abstract Syntax Trees."""
    
    def __init__(self, source: Union[FrameType, str]):
        self.source = getsource(source) if isinstance(source, FrameType) else source

    def build(self) -> Optional[Tree]:
        if not self.source:
            return None
        
        tree = ast.parse(dedent(self.source))
        return self._build_tree_from_ast(tree)

    def _build_tree_from_ast(self, ast_tree: ast.AST) -> Optional[Tree]:
        tree = Tree(self.source)
        root_pos = Position(0, len(self.source))
        tree.root = Leaf(root_pos, {"type": "Module", "name": "Module"})

        for node in ast.walk(ast_tree):
            if hasattr(node, 'lineno'):
                position = Position(node.lineno, getattr(node, 'end_lineno', node.lineno))
                info = {"type": node.__class__.__name__}
                if hasattr(node, 'name'):
                    info["name"] = node.name
                leaf = Leaf(position, info)
                tree.add_leaf(leaf)

        return tree

class FrameAnalyzer:
    """Analyzes Python stack frames and builds tree representations."""
    
    def __init__(self, frame: Optional[FrameType]):
        self.frame = frame
        self.frame_position = Position(frame) if frame else Position(0, 0)
        self.ast_builder = AstTreeBuilder(frame) if frame else None
        self.tree = None
        self.current_node = None

    def find_current_node(self) -> Optional[Leaf]:
        if not self.tree:
            self.build_tree()
        
        if not self.tree or not self.tree.root:
            return None

        if self.current_node is None:
            matching_nodes = []
            for node in self.tree.flatten():
                if node.start is not None and node.end is not None:
                    distance = (abs(node.start - (self.frame_position.start or 0)) + 
                              abs(node.end - (self.frame_position.end or 0)))
                    matching_nodes.append((node, distance))

            if matching_nodes:
                self.current_node = min(matching_nodes, key=lambda x: x[1])[0]

        return self.current_node

    def build_tree(self) -> Optional[Tree]:
        if self.ast_builder:
            self.tree = self.ast_builder.build()
            if not self.tree:
                return None
            self.find_current_node()
        return self.tree

# Example usage
if __name__ == "__main__":
    # Create a tree
    tree = Tree("Example")
    root = Leaf(Position(0, 100), "Root")
    child1 = Leaf(Position(10, 50), "Child 1")
    child2 = Leaf(Position(60, 90), "Child 2")

    # Build tree structure
    tree.root = root
    root.add_child(child1)
    root.add_child(child2)

    # Visualize
    config = VisualizationConfig(show_info=True, show_size=True)
    tree.visualize(config)
