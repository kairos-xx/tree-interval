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

### 🎯 `tree_interval.rich_printer` 

#### `RichStyle` Class
*Configuration for node styling*

Properties:
- `color` (`str`): Color name or hex code
- `bold` (`bool`): Bold text styling

#### `LeafStyle` Class
*Tuple-based styling configuration*

Properties:
- `color` (`str`): Color hex code
- `bold` (`bool`): Bold text styling (default: False)

#### 🎨 `tree_interval.visualizer`

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
### Top Statement Property

The `top_statement` property allows finding the closest parent node that represents a complete statement according to AST_TYPES. This is particularly useful when working with complex expressions and needing to find their containing statement.

```python
# Example: result = obj.method().value
attribute_node.top_statement  # Returns the Assign node
```

Properties:
- Returns the nearest parent node that is marked as a statement in AST_TYPES
- Returns None if no statement parent is found
- The node itself is returned if it is a statement
## Statement API

### PartStatement
```python
@dataclass
class PartStatement:
    before: str  # Text before a statement part
    after: str   # Text after a statement part
```

### Statement
```python
@dataclass
class Statement:
    top: PartStatement     # Top level statement parts (e.g. print())
    before: str           # Text before current node (e.g. a.b.)
    self: str            # Current node text (e.g. d)
    after: str           # Text after current node (e.g. .e)
    
    # Marker characters
    top_marker: str = "^"      # For top statement parts
    chain_marker: str = "~"    # For chained parts
    current_marker: str = "*"  # For current node
    
    @property
    def text(self) -> str:
        """Get statement text with default markers"""
        return self.as_text()
        
    def as_text(self, top_marker=None, chain_marker=None, current_marker=None) -> str:
        """Get statement text with custom markers"""
```
