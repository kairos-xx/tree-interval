"""Unit tests for Tree Interval core functionality."""

import pytest

from src.tree_interval import AstTreeBuilder, FrameAnalyzer, Leaf, Position, Tree


def test_position_creation():
    pos = Position(0, 100, "Test")
    assert pos.start == 0
    assert pos.end == 100
    assert pos.info == "Test"
    assert pos.lineno is None


def test_position_line_info():
    pos = Position(0, 100, "Test")
    pos.lineno = 1
    pos.end_lineno = 5
    assert pos.lineno == 1
    assert pos.end_lineno == 5


def test_leaf_creation():
    pos = Position(0, 100, "Root")
    leaf = Leaf(pos)
    assert leaf.start == 0
    assert leaf.end == 100
    assert leaf.info == "Root"


def test_tree_creation():
    tree = Tree("Test")
    assert tree.source == "Test"
    assert tree.root is None


def test_tree_add_leaf():
    tree = Tree("Test")
    root = Leaf(Position(0, 100, "Root"))
    child = Leaf(Position(10, 50, "Child"))

    tree.root = root
    tree.add_leaf(child)

    assert len(root.children) == 1
    assert child.parent == root


def test_find_best_match():
    tree = Tree("Test")
    root = Leaf(Position(0, 100, "Root"))
    child = Leaf(Position(10, 50, "Child"))

    tree.root = root
    tree.add_leaf(child)

    match = tree.find_best_match(15, 45)
    assert match == child


def test_ast_builder():
    code = "x = 1 + 2"
    builder = AstTreeBuilder(code)
    tree = builder.build()
    assert tree is not None
    assert tree.root is not None


def test_frame_analyzer():
    def sample_func():
        frame = sample_func.__code__
        analyzer = FrameAnalyzer(frame)
        return analyzer.build_tree()

    tree = sample_func()
    assert tree is not None


def test_tree_serialization():
    tree = Tree("Test")
    root = Leaf(Position(0, 100, "Root"))
    tree.root = root

    json_str = tree.to_json()
    loaded_tree = Tree.from_json(json_str)

    assert loaded_tree.source == tree.source
    assert loaded_tree.root is not None and tree.root is not None
    assert loaded_tree.root.start == tree.root.start
    assert loaded_tree.root.end == tree.root.end


def test_leaf_hierarchy():
    root = Leaf(Position(0, 100, "Root"))
    child1 = Leaf(Position(10, 40, "Child1"))
    child2 = Leaf(Position(50, 90, "Child2"))
    grandchild = Leaf(Position(15, 35, "Grandchild"))

    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(grandchild)

    assert len(root.children) == 2
    assert len(child1.children) == 1
    assert grandchild.parent == child1


def test_find_parent():
    tree = Tree("Test")
    root = Leaf(Position(0, 100, {"type": "Module"}))
    child = Leaf(Position(10, 90, {"type": "FunctionDef"}))
    grandchild = Leaf(Position(20, 80, {"type": "Assign"}))
    
    tree.root = root
    tree.add_leaf(child)
    child.add_child(grandchild)
    
    found = grandchild.find_parent(lambda n: n.info.get("type") == "FunctionDef")
    assert found == child

def test_find_child():
    tree = Tree("Test")
    root = Leaf(Position(0, 100, {"type": "Module"}))
    child1 = Leaf(Position(10, 50, {"type": "FunctionDef"}))
    child2 = Leaf(Position(60, 90, {"type": "ClassDef"}))
    grandchild = Leaf(Position(20, 40, {"type": "Assign"}))
    
    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)
    child1.add_child(grandchild)
    
    found = root.find_child(lambda n: n.info.get("type") == "Assign")
    assert found == grandchild

def test_find_sibling():
    tree = Tree("Test")
    root = Leaf(Position(0, 100, {"type": "Module"}))
    child1 = Leaf(Position(10, 50, {"type": "Import"}))
    child2 = Leaf(Position(60, 90, {"type": "FunctionDef"}))
    
    tree.root = root
    tree.add_leaf(child1)
    tree.add_leaf(child2)
    
    found = child1.find_sibling(lambda n: n.info.get("type") == "FunctionDef")
    assert found == child2

if __name__ == "__main__":
    pytest.main([__file__])
