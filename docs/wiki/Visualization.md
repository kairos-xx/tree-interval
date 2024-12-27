
# Visualization

Tree Interval provides two visualization methods:

## Basic Visualization
```python
tree.visualize()
```

## Rich Printing
```python
from tree_interval.rich_printer import RichTreePrinter, RichPrintConfig

printer = RichTreePrinter()
printer.print_tree(tree)
```

### Custom Configuration
```python
config = RichPrintConfig(
    show_info=True,
    show_size=True,
    show_position=True
)
printer = RichTreePrinter(config)
```
