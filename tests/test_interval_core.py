import pytest

from tree_interval import Leaf, Position
from tree_interval.core.interval_core import Tree


def test_leaf_statement_property():
    root = Leaf(Position(0, 100), info={"type": "Module"})
    child = Leaf(Position(10, 50), info={"type": "Call"})
    root.add_child(child)
    assert child.top_statement is not None


def test_leaf_attribute_chain():
    root = Leaf(Position(0, 100), info={"type": "Attribute"})
    child = Leaf(Position(10, 50), info={"type": "Name"})
    root.add_child(child)
    assert child.next_attribute is None
    assert root.previous_attribute is not None


def test_nested_attributes():
    leaf = Leaf(Position(0, 100), info={"type": "Module"})
    leaf.position.lineno = 1
    leaf.position.end_lineno = 5
    attrs = leaf._as_dict()
    assert attrs["position"]["lineno"] == 1
    assert attrs["position"]["end_lineno"] == 5


def test_leaf_serialization():
    leaf = Leaf(Position(0, 100), info={"name": "test"})
    leaf_dict = leaf._as_dict()
    assert leaf_dict["start"] == 0
    assert leaf_dict["end"] == 100
    assert leaf_dict["info"]["name"] == "test"


def test_position_edge_cases():
    with pytest.raises(ValueError):
        _ = Position(None, None)


def test_leaf_complex_operations():
    leaf = Leaf(Position(0, 100))
    leaf.selected = True
    assert leaf.selected
    assert leaf.size == 100

    # Test attribute chain
    leaf.info = {"type": "Attribute"}
    assert leaf.next_attribute is None
    assert leaf.previous_attribute is None


def test_tree_empty_operations():
    tree = Tree("")
    assert tree.flatten() == []
    tree_json = tree.to_json()
    assert Tree.from_json(tree_json).root is None


def test_complex_leaf_operations():
    leaf = Leaf(Position(0, 100))
    leaf.position.lineno = 1
    leaf.position.end_lineno = 5
    leaf.position.col_offset = 0
    leaf.position.end_col_offset = 10
    assert leaf.lineno == 1
    assert leaf.end_lineno == 5
    assert leaf.col_offset == 0
    assert leaf.end_col_offset == 10


def test_leaf_navigation():
    root = Leaf(Position(0, 100))
    child1 = Leaf(Position(10, 30))
    child2 = Leaf(Position(40, 60))
    root.add_child(child1)
    root.add_child(child2)
    assert child1.next == child2
    assert child2.previous == child1


def test_tree_serialization():
    tree = Tree("test")
    root = Leaf(Position(0, 100), info={"type": "root"})
    child = Leaf(Position(10, 50), info={"type": "child"})
    tree.root = root
    tree.add_leaf(child)

    json_str = tree.to_json()
    loaded_tree = Tree.from_json(json_str)
    assert loaded_tree.root is not None
    assert getattr(loaded_tree.root, "info", {}).get("type") == "root"


def test_position_overlaps():
    pos1 = Position(0, 50)
    pos2 = Position(40, 90)
    pos3 = Position(60, 100)
    assert pos1.overlaps(pos2)
    assert not pos1.overlaps(pos3)

def test_leaf_is_set():
    leaf = Leaf(Position(0, 100), info={"type": "Set"})
    assert leaf.is_set

def test_leaf_statement():
    root = Leaf(Position(0, 100), info={"type": "Call", "source": "test()", "cleaned_value": "test"})
    child = Leaf(Position(10, 50), info={"type": "Name", "source": "test", "cleaned_value": "test"})
    root.add_child(child)
    stmt = child.statement
    assert stmt.text is not None

def test_leaf_find_operations():
    root = Leaf(Position(0, 100))
    child1 = Leaf(Position(10, 30))
    child2 = Leaf(Position(40, 60))
    grandchild = Leaf(Position(15, 25))
    
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(grandchild)
    
    found = grandchild.find(lambda n: n.start == 40)
    assert found == child2

def test_leaf_next_previous():
    root = Leaf(Position(0, 100))
    child1 = Leaf(Position(10, 30))
    child2 = Leaf(Position(40, 60))
    root.add_child(child1)
    root.add_child(child2)
    
    assert child1.next == child2
    assert child2.previous == child1
    assert root.previous is None
    assert child2.next is None

def test_tree_add_duplicate_leaf():
    tree = Tree("test")
    leaf1 = Leaf(Position(0, 50), info="test")
    leaf2 = Leaf(Position(0, 50), info="test")
    
    tree.add_leaf(leaf1)
    tree.add_leaf(leaf2)  # Should not add duplicate
    assert len(tree.flatten()) == 1

def test_nested_attributes_missing():
    leaf = Leaf(Position(0, 100))
    assert leaf.attributes.nonexistent_attr is None

def test_position_with_none_values():
    pos = Position(0, 100)
    pos.lineno = None
    pos.end_lineno = None
    assert pos.end_lineno == 1  # Default fallback

def test_leaf_get_ancestors():
    root = Leaf(Position(0, 100))
    child = Leaf(Position(10, 50))
    grandchild = Leaf(Position(20, 40))
    
    root.add_child(child)
    child.add_child(grandchild)
    
    ancestors = grandchild.get_ancestors()
    assert len(ancestors) == 2
    assert ancestors[0] == child
    assert ancestors[1] == root

if __name__ == "__main__":
    pytest.main([__file__])
