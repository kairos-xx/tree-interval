
# Tree Interval

A Python package for managing and visualizing interval tree structures with AST analysis capabilities.

## Overview

Tree Interval provides tools for:
- Managing tree structures with position tracking
- AST (Abstract Syntax Tree) analysis
- Frame analysis for runtime code inspection
- Position-aware node tracking
- Customizable tree visualization
- JSON serialization/deserialization

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
