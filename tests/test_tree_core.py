import unittest
from src.tree_interval import Tree, Leaf, Position


class TestTreeCore(unittest.TestCase):

    def setUp(self):
        self.tree = Tree("Test")
        self.root = Leaf(0, 100, "root")
        self.child = Leaf(10, 50, "child")

    def test_add_leaf(self):
        self.tree.root = self.root
        self.tree.add_leaf(self.child)
        self.assertEqual(len(self.tree.root.children), 1)
        self.assertEqual(self.tree.root.children[0].info, "child")

    def test_find_best_match(self):
        self.tree.root = self.root
        self.tree.add_leaf(self.child)
        match = self.tree.find_best_match(20, 30)
        self.assertEqual(match.info, "child")


if __name__ == '__main__':
    unittest.main()
