import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_multiple_parents(self):
        child_node = LeafNode(None, "child node 1")
        child_node2 = LeafNode("b", "child node 2")
        parent_node = ParentNode("span", [child_node])
        parent_node2 = ParentNode("div", [child_node2])
        grandparent_node = ParentNode("p", [parent_node, parent_node2])
        self.assertEqual(
            grandparent_node.to_html(),
            "<p><span>child node 1</span><div><b>child node 2</b></div></p>"
        )
    
    def test_to_html_with_multiple_children(self):
        child_node = LeafNode(None, "child1")
        child_node2 = LeafNode("b", "child2")
        child_node3 = LeafNode("i", "child3")
        parent_node = ParentNode("p", [child_node, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), "<p>child1<b>child2</b><i>child3</i></p>")

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("p", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()