import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("div", "Hello World")
        self.assertEqual(node.to_html(), "<div>Hello World</div>")