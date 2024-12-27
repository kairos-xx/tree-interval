
# Tree Interval API Reference

## Table of Contents
- [Core Package](#core-package)
  - [Tree](#tree)
  - [Leaf](#leaf)
  - [Position](#position)
- [Visualization](#visualization)
  - [TreeVisualizer](#treevisualizer)
  - [VisualizationConfig](#visualizationconfig)
- [Analysis](#analysis)
  - [AstTreeBuilder](#asttreebuilder)
  - [FrameAnalyzer](#frameanalyzer)

## Core Package

### Tree
The main tree structure implementation for managing interval-based hierarchies.

#### Constructor
```python
Tree(source: T, start_lineno: Optional[int] = None, indent_size: int = 4)
```

#### Methods
- **add_leaf(leaf: Leaf) -> None**
  - Adds a leaf to the tree structure
  - Parameters:
    - `leaf`: The leaf node to add

- **find_best_match(start: int, end: int) -> Optional[Leaf]**
  - Finds the best matching leaf for given position
  - Returns: Best matching leaf or None

- **find_parent(criteria: callable) -> Optional[Leaf]**
  - Finds first parent node matching the given criteria function
  - Parameters:
    - `criteria`: Function that takes a Leaf node and returns bool
  - Returns: Matching parent node or None

- **find_child(criteria: callable) -> Optional[Leaf]**
  - Finds first child node matching the given criteria function
  - Parameters:
    - `criteria`: Function that takes a Leaf node and returns bool
  - Returns: Matching child node or None

- **find_sibling(criteria: callable) -> Optional[Leaf]**
  - Finds first sibling node matching the given criteria function
  - Parameters:
    - `criteria`: Function that takes a Leaf node and returns bool
  - Returns: Matching sibling node or None

### Leaf
Represents a node in the tree structure.

#### Constructor
```python
Leaf(position: Union[Position, tuple[int, int, Any]])
```

#### Methods
- **add_child(child: Leaf) -> None**
  - Adds a child node
  - Parameters:
    - `child`: Child node to add

### Position
Manages position information for tree nodes.

#### Constructor
```python
Position(start: int, end: int, info: Any)
```

#### Properties
- `lineno`: Starting line number
- `end_lineno`: Ending line number
- `col_offset`: Starting column offset
- `end_col_offset`: Ending column offset

## Visualization

### TreeVisualizer
Handles tree structure visualization.

#### Methods
- **visualize(tree: Tree, config: Optional[VisualizationConfig] = None) -> None**
  - Visualizes the tree structure
  - Parameters:
    - `tree`: Tree to visualize
    - `config`: Optional visualization configuration

### VisualizationConfig
Configuration for tree visualization.

#### Constructor
```python
VisualizationConfig(
    show_info: bool = True,
    show_size: bool = True,
    show_children_count: bool = False,
    position_format: str = "range"
)
```

## Analysis

### AstTreeBuilder
Builds tree structures from Python AST. See [AST Reference](AST_REFERENCE.md) for detailed documentation.

#### Methods
- **build() -> Tree**
  - Builds and returns AST tree

### FrameAnalyzer
Analyzes Python stack frames.

#### Methods
- **find_current_node() -> Optional[Leaf]**
  - Finds current AST node
- **build_tree() -> Optional[Tree]**
  - Builds tree from frame
