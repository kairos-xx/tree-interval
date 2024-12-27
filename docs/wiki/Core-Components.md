
# Core Components

## Position
The `Position` class manages position information for tree nodes:
```python
position = Position(start=0, end=100, info="Example")
position.lineno = 1
position.end_lineno = 5
```

## Leaf
Represents a node in the tree structure:
```python
leaf = Leaf(Position(0, 100, "Node Info"))
```

## Tree
Main container class managing the tree structure:
```python
tree = Tree(source="Example Code")
tree.add_leaf(leaf)
```
