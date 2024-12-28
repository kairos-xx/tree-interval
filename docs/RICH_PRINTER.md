
# Rich Tree Printer

## Related Documentation
- [README](README.md): Overview and implementation details
- [API Reference](API_REFERENCE.md): Core API documentation
- [AST Reference](AST_REFERENCE.md): AST analysis documentation

The Rich Tree Printer module provides enhanced tree visualization using the Rich library.

## Quick Start

```python
from tree_interval import Tree, Leaf, Position
from tree_interval.rich_printer import RichTreePrinter

# Create a tree
tree = Tree("Example")
root = Leaf(Position(0, 100), "Root")
tree.root = root

# Print using Rich
printer = RichTreePrinter()
printer.print_tree(tree)
```

## Configuration

Use `RichPrintConfig` to customize the visualization:

```python
from tree_interval.rich_printer import RichPrintConfig
from rich.style import Style

config = RichPrintConfig(
    show_info=True,          # Show node info
    show_size=True,          # Show node size
    show_position=True,      # Show position intervals
    indent_size=2,           # Indentation size
    root_style=Style(color="green", bold=True),
    node_style=Style(color="blue"),
    leaf_style=Style(color="cyan")
)

printer = RichTreePrinter(config)
```

## Features

- Colored output with customizable styles
- Tree structure visualization with guide lines
- Configurable node information display
- Support for position intervals and sizes
- Customizable indentation

## Usage Examples

### Basic Tree
```python
tree = Tree("Example")
root = Leaf(Position(0, 100), {"type": "Root"})
child = Leaf(Position(10, 50), {"type": "Child"})
tree.root = root
tree.add_leaf(child)

printer = RichTreePrinter()
printer.print_tree(tree)
```

### Custom Styles
```python
config = RichPrintConfig(
    root_style=Style(color="magenta", bold=True),
    node_style=Style(color="yellow"),
    leaf_style=Style(color="green")
)
printer = RichTreePrinter(config)
```

### AST Visualization
```python
tree = Tree("AST")
root = Leaf(Position(0, 100), {"type": "Module"})
func = Leaf(Position(10, 90), {"type": "Function", "name": "main"})
tree.root = root
tree.add_leaf(func)

printer = RichTreePrinter(RichPrintConfig(show_position=False))
printer.print_tree(tree)
```
