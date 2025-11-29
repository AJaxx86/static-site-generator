import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Some bold text")
        self.assertEqual(node.to_html(), "<b>Some bold text</b>")

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "This should be italics")
        self.assertEqual(node.to_html(), "<i>This should be italics</i>")
    
    def test_leaf_to_html_raw(self):
        node = LeafNode("", "This is some raw text")
        self.assertEqual(node.to_html(), "This is some raw text")