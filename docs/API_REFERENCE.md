
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

<<<<<<< HEAD
#### Methods
- **position_as(position_format: str = "default") -> str**
  - Returns a string representation of the position in different formats
  - Parameters:
    - `position_format`: Format type ("position", "tuple", or "default")
  - Returns: Formatted string of position information

=======
>>>>>>> 151f403bd09e889cfadedf4c57cd8af99003b1b7
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
Converts Python source code or frame objects into Tree Interval's tree structure.

#### Constructor
```python
AstTreeBuilder(source: Union[FrameType, str])
```
- Parameters:
  - `source`: Either Python source code as string or a frame object

#### Methods
- **build() -> Tree[str]**
  - Parses source code into AST and converts to tree structure
  - Returns: Tree with nodes containing AST information
  - Each node contains:
    - Position information (start, end, line numbers)
    - AST node type
    - Node-specific fields (name, args, etc.)

### FrameAnalyzer
Analyzes Python stack frames for runtime code inspection.

#### Constructor
```python
FrameAnalyzer(frame: FrameType)
```
- Parameters:
  - `frame`: Python stack frame to analyze

#### Methods
- **find_current_node() -> Optional[Leaf]**
  - Locates AST node for current execution point
  - Returns: Leaf node at current line or None
  - Useful for runtime code analysis

- **build_tree() -> Optional[Tree]**
  - Constructs complete tree from frame's source
  - Returns: Full AST tree or None if source unavailable
  - Includes all code in frame's scope
