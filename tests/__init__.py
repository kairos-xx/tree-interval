"""Tests for the tree-visualizer package."""

import pytest


# Run all tests
def run_tests():
    pytest.main(
        [
            "tests/test_tree_core.py",
            "tests/test_rich_printer.py",
            "tests/test_ast_nodes.py",
        ]
    )


if __name__ == "__main__":
    run_tests()
