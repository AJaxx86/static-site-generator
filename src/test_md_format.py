import unittest
from md_format import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This should test **bold** text.", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_node, [TextNode("This should test ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" text.", TextType.TEXT)])
    
    def test_italic(self):
        node = TextNode("This is _italic_ text.", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_node, [TextNode("This is ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" text.", TextType.TEXT)])
    
    def test_code(self):
        node = TextNode("This is `code` text.", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_node, [TextNode("This is ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" text.", TextType.TEXT)])\
    
    def test_first_and_last_delimiter(self):
        node = TextNode("**ANNOUNCEMENT** For all users! We are having a **SALE!**", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_node, [TextNode("ANNOUNCEMENT", TextType.BOLD), TextNode(" For all users! We are having a ", TextType.TEXT), TextNode("SALE!", TextType.BOLD)])

    def test_multiple_nodes(self):
        nodes = [
            TextNode("WARNING!", TextType.BOLD),
            TextNode("This is a _warning_ for something", TextType.TEXT),
            TextNode("All warnings should be taken very seriously.", TextType.ITALIC)
        ]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("WARNING!", TextType.BOLD), TextNode("This is a ", TextType.TEXT), TextNode("warning", TextType.ITALIC), TextNode(" for something", TextType.TEXT), TextNode("All warnings should be taken very seriously.", TextType.ITALIC)])
    
    def test_multiple_occurances(self):
        node = TextNode("This **text** contains **multiple** different string **types.**", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_node, [TextNode("This ", TextType.TEXT), TextNode("text", TextType.BOLD), TextNode(" contains ", TextType.TEXT), TextNode("multiple", TextType.BOLD), TextNode(" different string ", TextType.TEXT), TextNode("types.", TextType.BOLD)])

    def test_multiple_nodes_and_occurances(self):
        nodes = [
            TextNode("**LISTEN UP PRIVATE!** No shinanigans will be **TOLERATED** on this vessel!", TextType.TEXT),
            TextNode("Did you hear me?", TextType.BOLD),
            TextNode("I SAID **NO SHENANIGANS!** ON MY **DAMN VESSEL!** YA HEAR ME?!", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("LISTEN UP PRIVATE!", TextType.BOLD), TextNode(" No shinanigans will be ", TextType.TEXT), TextNode("TOLERATED", TextType.BOLD), TextNode(" on this vessel!", TextType.TEXT), TextNode("Did you hear me?", TextType.BOLD), TextNode("I SAID ", TextType.TEXT), TextNode("NO SHENANIGANS!", TextType.BOLD), TextNode(" ON MY ", TextType.TEXT), TextNode("DAMN VESSEL!", TextType.BOLD), TextNode(" YA HEAR ME?!", TextType.TEXT)])

    def test_close_delimiters(self):
        node = TextNode("Testing **close** **delimiters** for testing purposes.", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        print(f"Close delimiter test result: {new_node}")
        self.assertEqual(new_node, [TextNode("Testing ", TextType.TEXT), TextNode("close", TextType.BOLD), TextNode(" ", TextType.TEXT), TextNode("delimiters", TextType.BOLD), TextNode(" for testing purposes.", TextType.TEXT)])

    def test_missing_delimiter(self):
        node = TextNode("This is a _warning for missing formatting", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "_", TextType.ITALIC)
