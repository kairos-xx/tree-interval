
# Visualization

Tree Interval provides multiple visualization options:

## Basic ASCII Tree

Simple tree visualization with ANSI colors:

```python
tree.visualize()
```

Output:
```
┌── Position(0, 100) type=Module
├── Position(10, 40) type=FunctionDef name=hello
└── Position(50, 90) type=ClassDef name=Example
```

## Rich Pretty Printing

Enhanced visualization using the Rich library:

```python
from tree_interval.rich_printer import RichTreePrinter, RichPrintConfig

# Custom configuration
config = RichPrintConfig(
    show_info=True,
    show_size=True,
    show_position=True,
    indent_size=2
)

# Print tree
printer = RichTreePrinter(config)
printer.print_tree(tree)
```

## Customization Options

1. **Position Format**:
   - Full position details
   - Simple tuple format
   - Custom formatting

2. **Display Options**:
   - Node sizes
   - Type information  
   - Children counts
   - Custom node info

3. **Styling**:
   - Custom colors
   - Bold/italic text
   - Guide line styles
   - Indentation control

## Custom Root Visualization

Visualize tree from any node:

```python
# Using TreeVisualizer
tree.visualize(root=some_leaf)

# Using RichTreePrinter
printer = RichTreePrinter()
printer.print_tree(tree, root=some_leaf)
```

This allows viewing subtrees starting from any node in the tree structure.
