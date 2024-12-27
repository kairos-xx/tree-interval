
# Core Components

## Position

The `Position` class is the foundation for tracking node locations:

```python
from tree_interval import Position

# Basic position
pos = Position(start=0, end=100, info="Example")

# With line numbers
pos.lineno = 1
pos.end_lineno = 5

# With column offsets
pos.col_offset = 4
pos.end_col_offset = 24

# Access metrics
print(f"Size: {pos.size}")  # 100
print(f"Span: {pos.lineno}-{pos.end_lineno}")  # 1-5
```

## Leaf 

Leaf nodes form the tree structure:

```python
from tree_interval import Leaf

# Create hierarchy
root = Leaf(Position(0, 100, "Root"))
child = Leaf(Position(10, 50, "Child"))
root.add_child(child)

# Navigation
parent = child.parent  # Get parent
siblings = child.siblings  # Get siblings
children = root.children  # Get children

# Search
func_node = root.find(lambda n: n.info.get("type") == "FunctionDef")
parent = child.find_parent(lambda n: n.info.get("type") == "Module")
```

## Tree

The main container class:

```python
from tree_interval import Tree

# Create tree
tree = Tree(source="Example Code")
tree.root = root

# Find nodes
node = tree.find_best_match(25, 35)  # Find by position

# Serialization
json_str = tree.to_json()
loaded = Tree.from_json(json_str)
```

## AST Builder

Build trees from Python AST:

```python
from tree_interval import AstTreeBuilder

code = """
def hello():
    return "world"
"""

builder = AstTreeBuilder(code)
tree = builder.build()
```

## Frame Analyzer

Analyze runtime code positions:

```python
from tree_interval import FrameAnalyzer
import sys

frame = sys._getframe()
analyzer = FrameAnalyzer(frame)

# Get current node
node = analyzer.find_current_node()
```
