
# Tree Interval

A Python package for managing and visualizing interval tree structures with AST analysis capabilities.

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

## Repository Links
- GitHub: [https://github.com/kairos-xx/tree-interval](https://github.com/kairos-xx/tree-interval)
- PyPI: [https://pypi.org/project/tree-interval/](https://pypi.org/project/tree-interval/)

## Features
- Tree structure management with position tracking
- AST (Abstract Syntax Tree) analysis
- Frame analysis for runtime code inspection
- Position-aware node tracking
- Customizable tree visualization
- JSON serialization/deserialization

## License
MIT License - See LICENSE file for details
