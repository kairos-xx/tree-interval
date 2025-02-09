
# Tree Interval AST Reference

## Related Documentation
- [README](README.md): Overview and implementation details
- [API Reference](API_REFERENCE.md): Core API documentation
- [Rich Printer Guide](RICH_PRINTER.md): Advanced visualization options

## Overview
Tree Interval provides comprehensive AST (Abstract Syntax Tree) analysis capabilities through the `AstTreeBuilder` class and related utilities.

## AstTreeBuilder
The main class for converting Python code into Tree Interval's tree structure.

### Constructor
```python
AstTreeBuilder(source: Union[FrameType, str])
```

### Methods
- **build() -> Tree[str]**
  - Converts source code into a tree structure
  - Returns: Tree representation of the AST

### Node Information
Each AST node contains:
- `type`: The AST node type (e.g., "Module", "FunctionDef", "If")
- `fields`: Dictionary of node-specific attributes
- `_fields`: Raw AST node fields data
- `ast_node`: Direct access to underlying AST node
Common fields include:
  - `name`: For function and class definitions
  - `args`: For function arguments
  - `body`: For statement blocks
  - `test`: For conditional statements

## AST Node Types
Common node types and their fields:

### Module
Root node representing the entire source file
```python
{"type": "Module", "fields": {"body": "List[n]"}}
```

### FunctionDef
Function definition nodes
```python
{"type": "FunctionDef", "fields": {"name": "function_name", "args": "Arguments"}}
```

### If
Conditional statements
```python
{"type": "If", "fields": {"test": "Compare", "body": "List[n]", "orelse": "List[n]"}}
```

### Call
Function calls
```python
{"type": "Call", "fields": {"func": "Name", "args": "List[n]"}}
```

## Example Usage
```python
from tree_interval import AstTreeBuilder

# Parse Python code
code = """
def example(x):
    if x > 0:
        return x * 2
    return 0
"""

builder = AstTreeBuilder(code)
ast_tree = builder.build()
ast_tree.visualize()
```

## Related Documentation
- [Main API Reference](API_REFERENCE.md)
- [Frame Analysis](FRAME_REFERENCE.md)
