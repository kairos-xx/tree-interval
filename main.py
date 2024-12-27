
"""Main entry point for the tree-interval package demo."""
from examples.demo import (
    demonstrate_positions,
    demonstrate_leaves,
    demonstrate_tree_operations,
    example_basic_tree,
    example_custom_visualization,
    example_json_serialization,
    demonstrate_line_positions,
)

if __name__ == "__main__":
    print("=== Tree Interval Package Demo ===")
    demonstrate_positions()
    demonstrate_leaves()
    demonstrate_tree_operations()
    example_basic_tree()
    example_custom_visualization()
    example_json_serialization()
    demonstrate_line_positions()
