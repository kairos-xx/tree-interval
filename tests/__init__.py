"""Tests for the tree-visualizer package."""

import pytest


# Run all tests
def run_tests():
    pytest.main([
        "tests/test_ast_builder.py",
        "tests/test_ast_nodes.py",
        "tests/test_frame_analyzer.py",
        "tests/test_future.py",
        "tests/test_interval_core.py",
        "tests/test_rich_printer.py",
        "tests/test_styling.py",
        "tests/test_tree_core.py",
        "tests/test_visualizer.py",
    ])


if __name__ == "__main__":
    run_tests()
