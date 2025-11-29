import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a text node", TextType.PLAIN)
        self.assertEqual(node, node2)
    
    def test_ne(self):
        node = TextNode("This is also a text node", TextType.PLAIN)
        node2 = TextNode("That should pass", TextType.PLAIN)
        self.assertNotEqual(node, node2)
    
    def test_text_type(self):
        node = TextNode("This is testing bold text", TextType.PLAIN)
        node2 = TextNode("This is testing bold text", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_url(self):
        node = TextNode("This is testing url text", TextType.ITALIC)
        node2 = TextNode("This is testing url text", TextType.ITALIC, "https://www.google.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()