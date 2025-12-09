import unittest
from md_format import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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
        self.assertEqual(new_node, [TextNode("Testing ", TextType.TEXT), TextNode("close", TextType.BOLD), TextNode(" ", TextType.TEXT), TextNode("delimiters", TextType.BOLD), TextNode(" for testing purposes.", TextType.TEXT)])

    def test_missing_delimiter(self):
        node = TextNode("This is a _warning for missing formatting", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "_", TextType.ITALIC)

    def test_extract_md_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_md_links(self):
        matches = extract_markdown_links(
            "Go to [Google](https://google.com) for more information."
        )
        self.assertListEqual([("Google", "https://google.com")], matches)
    
    def test_extract_multiple_md_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_md_links(self):
        matches = extract_markdown_links(
            "Go to [Google](https://google.com) and [GitHub](https://github.com) for more information."
        )
        self.assertListEqual([("Google", "https://google.com"), ("GitHub", "https://github.com")], matches)
    
    def test_no_md_images(self):
        matches = extract_markdown_images("This is text with no images.")
        self.assertListEqual([], matches)
    
    def test_no_md_links(self):
        matches = extract_markdown_links("This is text with no links.")
        self.assertListEqual([], matches)
        
    def test_extract_md_images_ignores_links(self):
        matches = extract_markdown_images("This is text with a [link](https://google.com).")
        self.assertListEqual([], matches)
    
    def test_extract_md_links_ignores_images(self):
        matches = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png).")
        self.assertListEqual([], matches)
    
    def test_extract_empty_md_images(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)
    
    def test_extract_empty_md_links(self):
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://amazon.com) and another [second link](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://amazon.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://google.com"),
            ],
            new_nodes,
        )
    
    def test_multiple_nodes_split_images(self):
        nodes = [
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            ),
            TextNode(
                "This node contains ![tons](https://i.imgur.com/3elNhQu.png) of ![images](https://i.imgur.com/zjjcJKZ.png), like ![this one](https://i.imgur.com/zjjcJKZ.png) and ![also this one](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            ),
            TextNode(
                "One last node with ![some](https://i.imgur.com/3elNhQu.png) more ![images](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT
            ),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                ],
                [
                TextNode("This node contains ", TextType.TEXT),
                TextNode("tons", TextType.TEXT),
                TextNode(" of ", TextType.TEXT),
                TextNode("images", TextType.TEXT),
                TextNode(" like ", TextType.TEXT),
                TextNode("this one", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("also this one", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                ],
                [
                TextNode("One last node with ", TextType.TEXT),
                TextNode("some", TextType.TEXT),
                TextNode(" more ", TextType.TEXT),
                TextNode("images", TextType.TEXT),
                ],
            ],
            new_nodes,
        )