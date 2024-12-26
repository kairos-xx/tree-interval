
# Tree Visualizer

A Python package for building and visualizing tree structures with support for AST analysis.

## Features
- Tree data structure implementation
- AST analysis and visualization
- Customizable tree visualization
- JSON serialization support

## Installation
```bash
pip install tree-visualizer
```

## Usage
```python
from tree_visualizer import Tree, Leaf, TreeVisualizer

# Create a tree
tree = Tree("Example")
root = Leaf(0, 100, "root")
tree.root = root

# Add children
child = Leaf(10, 50, "child")
tree.add_leaf(child)

# Visualize
tree.visualize()
```
