
"""Tests for the tree-visualizer package.

This package contains comprehensive test suites for validating the functionality
of the tree-interval package components including:
- AST building and parsing
- Frame analysis and position tracking
- Tree operations and manipulations 
- Visualization capabilities
- Rich printing functionality

The test organization follows the module structure with dedicated
test files for each major component.
"""

import pytest

def run_tests():
    """Run all test suites in the proper order.
    
    This function executes all test modules using pytest, ensuring proper
    coverage of all package functionality including:
    - AST builder tests
    - Node type tests
    - Frame analyzer tests 
    - Future object tests
    - Core interval functionality
    - Rich printer tests
    - Styling tests
    - Tree core operations
    - Visualizer functionality
    """
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
