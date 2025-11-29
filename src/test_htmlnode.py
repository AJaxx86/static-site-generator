import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(value="Testing props", props={"one": "1", "two": "2"})
        self.assertEqual(node.props_to_html(), ' one="1" two="2"')