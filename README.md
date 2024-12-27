
# Tree Interval

A Python package for managing and visualizing interval tree structures with AST analysis capabilities.

## Overview

Tree Interval provides tools for:
- Building and analyzing tree structures
- AST (Abstract Syntax Tree) parsing and visualization
- Frame analysis for runtime code inspection
- Position-aware node tracking
- Customizable tree visualization
- JSON serialization/deserialization

## Similar Packages
- `ast`: Python's built-in AST module (Tree Interval builds upon this)
- `anytree`: General purpose tree structures
- `treelib`: Tree data structure implementation

## Installation

```bash
pip install tree-interval
```

## Quick Start

```python
from tree_interval import Tree, Leaf, Position

# Create a basic tree
tree = Tree("Example")
root = Leaf(Position(0, 100, "Root"))
child = Leaf(Position(10, 50, "Child"))

tree.root = root
tree.add_leaf(child)

# Visualize the tree
tree.visualize()
```

## Features

### Node Search
```python
# Find parent with specific type
parent = node.find_parent(lambda n: n.info.get("type") == "FunctionDef")

# Find child with specific field value
child = node.find_child(lambda n: n.info.get("fields", {}).get("name") == "x")

# Find sibling with specific type
sibling = node.find_sibling(lambda n: n.info.get("type") == "If")
```

### Position-Aware Nodes
```python
position = Position(start=0, end=100, info="Root")
position.lineno = 1
position.end_lineno = 5
position.col_offset = 0
position.end_col_offset = 100
```

### AST Analysis
```python
from tree_interval import AstTreeBuilder

code = """
def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)
"""
builder = AstTreeBuilder(code)
ast_tree = builder.build()
ast_tree.visualize()
```

### Frame Analysis
```python
from tree_interval import FrameAnalyzer
import sys

frame = sys._getframe()
analyzer = FrameAnalyzer(frame)
current_node = analyzer.find_current_node()
```

## API Reference

### Tree
- `Tree(source: T, start_lineno: Optional[int] = None, indent_size: int = 4)`
- `add_leaf(leaf: Leaf) -> None`
- `find_best_match(start: int, end: int) -> Optional[Leaf]`
- `visualize(config: Optional[VisualizationConfig] = None) -> None`

### Leaf
- `Leaf(position: Union[Position, tuple[int, int, Any], int])`
- `add_child(child: Leaf) -> None`
- `find_best_match(start: int, end: int) -> Optional[Leaf]`

### Position
- `Position(start: Optional[int], end: Optional[int], info: Optional[Any])`
- Properties: `lineno`, `end_lineno`, `col_offset`, `end_col_offset`

## Potential Use Cases
- Code analysis tools
- Syntax highlighters
- Code structure visualization
- Runtime code inspection
- AST-based code transformations

## Limitations
- Memory usage scales with tree size
- Visualization may become cluttered with large trees
- AST analysis limited to Python code
- Frame analysis requires careful handling of stack frames

## License
MIT License - See LICENSE file for details
