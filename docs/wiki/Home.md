
# Tree Interval

A Python package for managing and visualizing interval tree structures with AST analysis capabilities.

## Navigation
- [Installation Guide](Installation.md)
- [Core Components](Core-Components.md)
- [Visualization Guide](Visualization.md)

## Documentation
- [API Reference](../tree/master/docs/API_REFERENCE.md)
- [AST Reference](../tree/master/docs/AST_REFERENCE.md)
- [Rich Printer Guide](../tree/master/docs/RICH_PRINTER.md)

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

## Related Topics
- For core components like Tree, Leaf, and Position, see [Core Components](Core-Components.md)
- For visualization options, check the [Visualization Guide](Visualization.md)
- For detailed API documentation, refer to the [API Reference](../docs/API_REFERENCE.md)
