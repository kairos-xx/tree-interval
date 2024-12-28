"""Unit tests for Tree Interval core functionality."""

import pytest

from src.tree_interval import Leaf, Position, Tree


def test_position_creation():
    pos = Position(0, 100)
    assert pos.start == 0
    assert pos.end == 100
    assert pos.info == "Test"
    assert pos.lineno is None


def test_position_line_info():
    pos = Position(0, 100)
    pos.lineno = 1
    pos.end_lineno = 5
    assert pos.lineno == 1
    assert pos.end_lineno == 5


def test_leaf_creation():
    pos = Position(0, 100)
    leaf = Leaf(pos, "Root")
    assert leaf.start == 0
    assert leaf.end == 100
    assert leaf.info == "Root"


def test_tree_creation():
    tree = Tree("Test")
    assert tree.source == "Test"
    assert tree.root is None


def test_tree_add_leaf():
    tree = Tree("Test")
    root = Leaf(Position(0, 100), "Root")
    child = Leaf(Position(10, 50), "Child")

    tree.root = root
    tree.add_leaf(child)

    assert len(root.children) == 1
    assert child.parent == root


def test_find_best_match():
    tree = Tree("Test")
    root = Leaf(Position(0, 100), "Root")
    child = Leaf(Position(10, 50), "Child")

    tree.root = root
    tree.add_leaf(child)

    match = tree.find_best_match(15, 45)
    assert match == child


def test_find_parent():
    root = Leaf(Position(0, 100), {"type": "Module"})
    child1 = Leaf(Position(10, 50), {"type": "FunctionDef"})
    grandchild = Leaf(Position(20, 40), {"type": "Return"})

    root.add_child(child1)
    child1.add_child(grandchild)

    found = grandchild.find_parent(lambda n: isinstance(n.info, dict) and n.
                                   info.get("type") == "FunctionDef")
    assert found == child1

    found = grandchild.find_parent(
        lambda n: isinstance(n.info, dict) and n.info.get("type") == "Module")
    assert found == root

    found = root.find_parent(
        lambda n: isinstance(n.info, dict) and n.info.get("type") == "Module")
    assert found is None


def test_find_child():
    root = Leaf(Position(0, 100), {"type": "Module"})
    child1 = Leaf(Position(10, 40), {"type": "Assign"})
    child2 = Leaf(Position(50, 90), {"type": "FunctionDef"})

    root.add_child(child1)
    root.add_child(child2)

    found = root.find_child(
        lambda n: n.info is not None and n.info.get("type") == "Assign")
    assert found == child1

    found = root.find_child(
        lambda n: n.info is not None and n.info.get("type") == "FunctionDef")
    assert found == child2

    found = child1.find_child(
        lambda n: n.info is not None and n.info.get("type") == "Assign")
    assert found is None


def test_find_sibling():
    root = Leaf(Position(0, 100), {"type": "Module"})
    child1 = Leaf(Position(10, 40), {"type": "Assign"})
    child2 = Leaf(Position(50, 90), {"type": "FunctionDef"})

    root.add_child(child1)
    root.add_child(child2)

    found = child1.find_sibling(
        lambda n: n.info is not None and n.info.get("type") == "FunctionDef")
    assert found == child2


def test_find():
    root = Leaf(Position(0, 100), {"type": "Module"})
    child1 = Leaf(Position(10, 40), {"type": "FunctionDef", "name": "hello"})
    child2 = Leaf(Position(50, 90), {"type": "ClassDef", "name": "MyClass"})
    grandchild = Leaf(Position(20, 30), {"type": "Return"})

    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(grandchild)

    # Find in current node

    found = root.find(
        lambda n: n.info is not None and n.info.get("type") == "Module")
    assert found == root

    # Find in parent
    found = grandchild.find(
        lambda n: n.info is not None and n.info.get("type") == "FunctionDef")
    assert found == child1

    # Find in children
    found = root.find(
        lambda n: n.info is not None and n.info.get("name") == "hello")
    assert found == child1

    # Find in siblings
    found = child1.find(
        lambda n: n.info is not None and n.info.get("name") == "MyClass")
    assert found == child2


def test_leaf_hierarchy():
    root = Leaf(Position(0, 100), "Root")
    child1 = Leaf(Position(10, 40), "Child1")
    child2 = Leaf(Position(50, 90), "Child2")
    grandchild = Leaf(Position(15, 35), "Grandchild")

    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(grandchild)

    assert len(root.children) == 2
    assert len(child1.children) == 1
    assert grandchild.parent == child1


def test_tree_serialization():
    tree = Tree("Test")
    root = Leaf(Position(0, 100), "Root")
    tree.root = root

    json_str = tree.to_json()
    loaded_tree = Tree.from_json(json_str)

    assert loaded_tree.source == tree.source
    assert loaded_tree.root is not None and tree.root is not None
    assert loaded_tree.root.start == tree.root.start
    assert loaded_tree.root.end == tree.root.end


def test_position_format():
    # Create root position
    root_pos = Position(0, 100)
    root_pos.lineno = 1
    root_pos.end_lineno = 10
    root_pos.col_offset = 0
    root_pos._end_col_offset = 80
    root = Leaf(root_pos)

    # Create child1 position
    child1_pos = Position(10, 40)
    child1_pos.lineno = 2
    child1_pos.end_lineno = 4
    child1_pos.col_offset = 4
    child1_pos.end_col_offset = 24  # End col offset for child1
    child1 = Leaf(child1_pos)

    # Create grandchild1 position
    grandchild1_pos = Position(15, 25)
    grandchild1_pos.lineno = 3
    grandchild1_pos.end_lineno = 3
    grandchild1_pos.col_offset = 8
    grandchild1_pos.end_col_offset = 28  # End col offset for grandchild1
    grandchild1 = Leaf(grandchild1_pos)

    # Create child2 position
    child2_pos = Position(50, 90)
    child2_pos.lineno = 5
    child2_pos.end_lineno = 8
    child2_pos.col_offset = 4
    child2_pos.end_col_offset = 24  # End col offset for child2
    child2 = Leaf(child2_pos)

    # Create grandchild2 position
    grandchild2_pos = Position(60, 80)
    grandchild2_pos.lineno = 6
    grandchild2_pos.end_lineno = 7
    grandchild2_pos.col_offset = 8
    grandchild2_pos.end_col_offset = 28  # End col offset for grandchild2
    grandchild2 = Leaf(grandchild2_pos)

    # Build tree structure
    root.add_child(child1)
    child1.add_child(grandchild1)
    root.add_child(child2)
    child2.add_child(grandchild2)

    # Verify positions and structure
    assert root.size == 100
    assert child1.size == 30
    assert grandchild1.size == 10
    assert child2.size == 40
    assert grandchild2.size == 20

    assert root.col_offset == 0
    assert root.end_col_offset == 80
    assert child1.col_offset == 4
    assert grandchild1.col_offset == 8
    assert child2.col_offset == 4
    assert grandchild2.col_offset == 8

    assert len(root.children) == 2
    assert len(child1.children) == 1
    assert len(child2.children) == 1


if __name__ == "__main__":
    pytest.main([__file__])


def test_node_navigation():
    root = Leaf(Position(0, 100), "Root")
    child1 = Leaf(Position(10, 40), "Child1")
    child2 = Leaf(Position(50, 90), "Child2")

    root.add_child(child1)
    root.add_child(child2)

    # Test parent relationship
    assert child1.parent == root
    assert child2.parent == root

    # Test next sibling
    assert child1.next == child2
    assert child2.next is None

    # Test previous sibling
    assert child2.previous == child1
    assert child1.previous is None
