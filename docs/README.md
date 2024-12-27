
# Tree Interval Technical Documentation

## Architecture Overview

### Core Components
- `interval_core.py`: Core tree data structures
- `ast_builder.py`: AST analysis functionality ([AST Reference](AST_REFERENCE.md))
- `frame_analyzer.py`: Runtime frame analysis

### Visualization
- `visualizer.py`: Tree rendering
- `config.py`: Visualization configuration ([Rich Printer Guide](RICH_PRINTER.md))

## Implementation Details

### Tree Structure
The tree implementation uses a parent-child relationship model with position awareness. Each node tracks:
- Start/end positions
- Line numbers
- Column offsets
- Parent/child relationships
(See [API Reference](API_REFERENCE.md) for detailed implementation)

### Position Tracking
Position objects maintain both absolute positions and source-relative positions:
```python
Position(
    start=10,          # Absolute start
    end=50,           # Absolute end
    info="Node",      # Node information
    lineno=2,         # Source line number
    end_lineno=3      # End line number
)
```

### AST Integration
The AST builder wraps Python's built-in `ast` module to:
1. Parse source code
2. Create position-aware nodes
3. Build hierarchical relationships
(See [AST Reference](AST_REFERENCE.md) for details)

### Frame Analysis
Frame analysis provides runtime code inspection by:
1. Extracting source from stack frames
2. Mapping positions to AST nodes
3. Building tree representations

## Best Practices

### Memory Management
- Clear unused trees
- Limit tree depth for large codebases
- Use weak references for circular structures

### Performance
- Cache position calculations
- Minimize tree reconstructions
- Use appropriate visualization configs

### Error Handling
- Validate position ranges
- Handle malformed AST gracefully
- Check frame availability

## Advanced Usage

### Custom Visualization
```python
config = VisualizationConfig(
    position_format="tuple",
    show_children_count=True,
    show_size=False
)
tree.visualize(config)
```
(See [Rich Printer Guide](RICH_PRINTER.md) for more visualization options)

### AST Analysis
```python
builder = AstTreeBuilder(source_code)
tree = builder.build()
for node in tree.flatten():
    if node.info == "FunctionDef":
        print(f"Found function at {node.position}")
```

### Frame Inspection
```python
analyzer = FrameAnalyzer(frame)
tree = analyzer.build_tree()
current = analyzer.find_current_node()
if current:
    print(f"Executing: {current.info}")
```
