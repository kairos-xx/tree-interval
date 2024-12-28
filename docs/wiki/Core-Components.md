from tree_interval import Position

# Basic position
pos = Position(start=0, end=100)  # Only requires start and end positions

# With line numbers (optional)
pos.lineno = 1  # Source line number (defaults to 1)
pos.end_lineno = 5  # End line number (defaults to 1)
pos.col_offset = 4  # Column offset (optional)
pos.end_col_offset = 24  # End column offset (optional)

# Access metrics
print(f"Size: {pos.end - pos.start}")  # 100
print(f"Span: {pos.lineno}-{pos.end_lineno}")  # 1-5