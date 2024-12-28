
# Core Components

## Position

The `Position` class is the foundation for tracking node locations:

```python
from tree_interval import Position

# Basic position
pos = Position(start=0, end=100)

# With line numbers
pos.lineno = 1
pos.end_lineno = 5

# With column offsets
pos.col_offset = 4
pos.end_col_offset = 24

# Access metrics
print(f"Size: {pos.end - pos.start}")  # 100
print(f"Span: {pos.lineno}-{pos.end_lineno}")  # 1-5
```

## Leaf 

Leaf nodes form the tree structure:

```python
from tree_interval import Leaf, Position

# Create hierarchy
root = Leaf(Position(0, 100), info="Root")
child = Leaf(Position(10, 50), info="Child")
root.add_child(child)

# Navigation
parent = child.parent  # Get parent
siblings = child.siblings  # Get siblings
children = root.children  # Get children

### Navigation Methods

The `Leaf` class provides methods for navigating between nodes:

```python
# Get parent node
parent = node.parent  # Returns parent node or None

# Get next sibling
next_sibling = node.next  # Returns next sibling or None

# Get previous sibling
prev_sibling = node.previous  # Returns previous sibling or None

# Example usage
if node.parent:
    print(f"Parent info: {node.parent.info}")
    
if node.next:
    print(f"Next sibling: {node.next.info}")
    
if node.previous:
    print(f"Previous sibling: {node.previous.info}")
```

# Search
func_node = root.find(lambda n: n.info.get("type") == "FunctionDef")
parent = child.find_parent(lambda n: n.info.get("type") == "Module")
```
