# Tree Interval API Reference

## Related Documentation
- [README](README.md): Overview and implementation details
- [AST Reference](AST_REFERENCE.md): AST analysis documentation
- [Rich Printer Guide](RICH_PRINTER.md): Advanced visualization options

## Core Modules

### 📦 `tree_interval.core.interval_core`

#### 📍 `Position` Class 
*Manages position information for tree nodes*

##### Methods

*  **`__init__(self, start: int, end: int) -> None`**  
Initializes a position with start and end positions.

Parameters:
- `start` (`int`): Start position (required)
- `end` (`int`): End position (required)

Properties:
- `lineno` (`int`): Source line number (optional, defaults to 1)
- `end_lineno` (`int`): End line number (optional, defaults to 1)
- `col_offset` (`Optional[int]`): Column offset (optional)
- `end_col_offset` (`Optional[int]`): End column offset (optional)

#### 🌳 `Leaf` Class
*Represents a node in the tree structure*

##### Methods

*  **`__init__(self, position: Union[Position, tuple[int, int, Any]]) -> None`**  
Initializes a leaf node.

Parameters:
- `position` (`Union[Position, tuple[int, int, Any]]`): Position information

*  **`add_child(self, child: 'Leaf') -> None`**  
Adds a child node to this leaf.

Parameters:
- `child` (`Leaf`): The child node to add

#### 🌲 `Tree` Class
*Main tree structure implementation*

##### Methods

*  **`__init__(self, source: str) -> None`**  
Initializes a new tree.

Parameters:
- `source` (`str`): Source identifier for the tree

*  **`add_leaf(self, leaf: Leaf) -> None`**  
Adds a leaf to the tree.

Parameters:
- `leaf` (`Leaf`): The leaf to add

*  **`find_best_match(self, start: int, end: int) -> Optional[Leaf]`**  
Finds the best matching leaf for given position.

Parameters:
- `start` (`int`): Start position
- `end` (`int`): End position

Returns:
- `Optional[Leaf]`: Best matching leaf or None

### 🎨 `tree_interval.visualizer`

#### `VisualizationConfig` Class
*Configuration settings for tree visualization*

##### Methods

*  **`__init__(self, show_info: bool = True, show_size: bool = True, show_children_count: bool = False, position_format: str = "range") -> None`**  
Initializes visualization configuration.

Parameters:
- `show_info` (`bool`): Whether to show node info
- `show_size` (`bool`): Whether to show node sizes
- `show_children_count` (`bool`): Whether to show children count
- `position_format` (`str`): Format for position display