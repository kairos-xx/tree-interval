
# Tree Interval

A powerful Python package for managing, analyzing and visualizing tree structures with rich interval-based node positioning.

## Key Features

- **Position-Aware Nodes**: Track code positions with line numbers, column offsets and intervals
- **AST Analysis**: Built-in support for Python AST traversal and node location
- **Frame Analysis**: Runtime code inspection with frame position tracking
- **Rich Visualization**: Multiple visualization options including ASCII trees and Rich-based pretty printing
- **JSON Serialization**: Full support for saving and loading tree structures
- **Flexible Node Search**: Parent, child and sibling search with custom predicates

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

## Core Concepts

### Position Types

1. **Basic Position**: Simple start/end interval
```python
pos = Position(0, 100, "Basic")
```

2. **Line-Aware Position**: Track line numbers
```python 
pos = Position(0, 100, "Lines")
pos.lineno = 1
pos.end_lineno = 5
```

3. **Column-Aware Position**: Full position tracking
```python
pos = Position(0, 100, "Columns")
pos.col_offset = 4
pos.end_col_offset = 8
```

### Node Search Methods

1. **Parent Search**:
```python
# Find parent node matching predicate
node.find_parent(lambda n: n.info.get("type") == "FunctionDef")
```

2. **Child Search**:
```python
# Find first child matching predicate 
node.find_child(lambda n: n.info.get("name") == "my_var")
```

3. **Sibling Search**:
```python
# Find sibling node
node.find_sibling(lambda n: n.info.get("type") == "ClassDef")
```

### Visualization Options

1. **Basic ASCII Tree**:
```python
tree.visualize()
```

2. **Rich Pretty Printing**:
```python
from tree_interval.rich_printer import RichTreePrinter
printer = RichTreePrinter()
printer.print_tree(tree)
```

## Similar Packages

- `ast`: Python's built-in AST module (Tree Interval adds position tracking)
- `asttokens`: Token-based AST analysis (Tree Interval provides richer interval model)
- `astroid`: Python AST framework (Tree Interval focuses on general tree structures)

## Use Cases

1. **Code Analysis**
   - Track source positions in AST nodes
   - Locate runtime code execution points
   - Analyze code structure and relationships

2. **Tree Visualization** 
   - Debug tree structures
   - Generate documentation
   - Analyze hierarchical data

3. **Position Tracking**
   - Map source locations
   - Track text positions
   - Handle nested intervals
