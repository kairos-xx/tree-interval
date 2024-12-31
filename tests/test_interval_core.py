

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
