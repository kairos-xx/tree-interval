
# Tree Interval

A Python package for managing and visualizing interval tree structures.

## Features
- Interval tree data structure implementation
- AST analysis and visualization
- Customizable interval visualization
- JSON serialization support

## Installation
```bash
pip install tree-interval
```

## Usage
```python
from tree_interval import IntervalTree, IntervalNode, TreeVisualizer

# Create a tree
tree = IntervalTree("Example")
root = IntervalNode(0, 100, "root")
tree.root = root

# Add children
child = IntervalNode(10, 50, "child")
tree.add_node(child)

# Visualize
tree.visualize()
```
