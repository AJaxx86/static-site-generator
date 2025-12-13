import unittest
from md_format import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
)
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
        self.assertEqual(new_node, [TextNode("This is ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" text.", TextType.TEXT)])
    
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

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_md_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_md_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_no_md_images(self):
        matches = extract_markdown_images("This is text with no images.")
        self.assertListEqual([], matches)

    def test_extract_md_images_ignores_links(self):
        matches = extract_markdown_images("This is text with a [link](https://google.com).")
        self.assertListEqual([], matches)

    def test_extract_empty_md_images(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_md_links(self):
        matches = extract_markdown_links(
            "Go to [Google](https://google.com) for more information."
        )
        self.assertListEqual([("Google", "https://google.com")], matches)

    def test_extract_multiple_md_links(self):
        matches = extract_markdown_links(
            "Go to [Google](https://google.com) and [GitHub](https://github.com) for more information."
        )
        self.assertListEqual([("Google", "https://google.com"), ("GitHub", "https://github.com")], matches)

    def test_no_md_links(self):
        matches = extract_markdown_links("This is text with no links.")
        self.assertListEqual([], matches)

    def test_extract_md_links_ignores_images(self):
        matches = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png).")
        self.assertListEqual([], matches)

    def test_extract_empty_md_links(self):
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)

class TestSplitNodesImage(unittest.TestCase):
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
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This node contains ", TextType.TEXT),
                TextNode("tons", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" of ", TextType.TEXT),
                TextNode("images", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(", like ", TextType.TEXT),
                TextNode("this one", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("also this one", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("One last node with ", TextType.TEXT),
                TextNode("some", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" more ", TextType.TEXT),
                TextNode("images", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_image_missing_parenthesis(self):
        node = TextNode("This should ![break(https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This should ![break(https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_only_image_text(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

    def test_adjacent_images(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_image_with_special_characters(self):
        node = TextNode("![I wonder* if this will break!](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("I wonder* if this will break!", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

    def test_image_with_non_text_node(self):
        node = TextNode("This is a bold ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is a bold ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

class TestSplitNodesLink(unittest.TestCase):
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

    def test_multiple_nodes_split_links(self):
        nodes = [
            TextNode(
                "This is text with a [link](https://amazon.com) and another [second link](https://google.com)",
                TextType.TEXT,
            ),
            TextNode(
                "This node contains [tons](https://amazon.com) of [links](https://google.com), like [this one](https://amazon.com) and [also this one](https://google.com)",
                TextType.TEXT,
            ),
            TextNode(
                "One last node with [some](https://amazon.com) more [links](https://google.com)",
                TextType.TEXT
            ),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://amazon.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://google.com"),
                TextNode("This node contains ", TextType.TEXT),
                TextNode("tons", TextType.LINK, "https://amazon.com"),
                TextNode(" of ", TextType.TEXT),
                TextNode("links", TextType.LINK, "https://google.com"),
                TextNode(", like ", TextType.TEXT),
                TextNode("this one", TextType.LINK, "https://amazon.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("also this one", TextType.LINK, "https://google.com"),
                TextNode("One last node with ", TextType.TEXT),
                TextNode("some", TextType.LINK, "https://amazon.com"),
                TextNode(" more ", TextType.TEXT),
                TextNode("links", TextType.LINK, "https://google.com"),
            ],
            new_nodes,
        )

    def test_link_missing_parenthesis(self):
        node = TextNode("This should ![break(https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This should ![break(https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_only_link_text(self):
        node = TextNode("[link](https://amazon.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://amazon.com")
            ],
            new_nodes,
        )

    def test_adjacent_links(self):
        node = TextNode("[link](https://amazon.com)[link](https://google.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("link", TextType.LINK, "https://amazon.com"),
                TextNode("link", TextType.LINK, "https://google.com"),
            ],
            new_nodes,
        )

    def test_link_with_special_characters(self):
        node = TextNode("[I wonder* if this will break!](https://amazon.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("I wonder* if this will break!", TextType.LINK, "https://amazon.com")
            ],
            new_nodes,
        )

    def test_link_with_non_text_node(self):
        node = TextNode("This is a bold [link](https://amazon.com)", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is a bold ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://amazon.com")
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ],
            nodes,
        )
    
    def test_text_to_textnodes_just_text(self):
        text = "Just some plain text without any fancy formatting."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            [TextNode("Just some plain text without any fancy formatting.", TextType.TEXT)],
            nodes
        )

    def test_text_to_textnodes_empty(self):
        with self.assertRaises(Exception):
            text_to_textnodes("")

    def test_text_to_textnodes_multiple_bolds(self):
        text = "This is **bold** and this is **also bold**."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and this is ", TextType.TEXT),
                TextNode("also bold", TextType.BOLD),
                TextNode(".", TextType.TEXT),
            ],
            nodes
        )
    
    def test_text_to_textnodes_adjacent_formatting(self):
        text = "**Bold**_Italic_`Code`"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("Bold", TextType.BOLD),
                TextNode("Italic", TextType.ITALIC),
                TextNode("Code", TextType.CODE),
            ],
            nodes
        )

    def test_text_to_textnodes_nested_order(self):
        text = "This is _italic_ and this is **bold**."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and this is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(".", TextType.TEXT),
            ],
            nodes
        )
    
    def test_text_to_textnodes_unclosed_bold(self):
        text = "This is **unclosed bold text"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_text_to_textnodes_unclosed_italic(self):
        text = "This is _unclosed italic text"
        with self.assertRaises(Exception):
            text_to_textnodes(text)
        
    def test_text_to_textnodes_links_and_formatting(self):
        text = "Click [here](https://boot.dev) or **boldly** go there."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://boot.dev"),
                TextNode(" or ", TextType.TEXT),
                TextNode("boldly", TextType.BOLD),
                TextNode(" go there.", TextType.TEXT),
            ],
            nodes
        )

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and [code](cci:1://file:///home/jaxx/workspace/boot.dev/static-site-generator/src/test_md_format.py:15:4-18:141) here
This is the same paragraph on a new line




- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and [code](cci:1://file:///home/jaxx/workspace/boot.dev/static-site-generator/src/test_md_format.py:15:4-18:141) here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_empty(self):
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])
    
    def test_markdown_to_blocks_whitespace(self):
        md = "   \n\n\n \n\n  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_markdown_to_blocks_trailing_whitespace(self):
        md = "  This is a block with leading spaces.   \n\nAnd this one has trailing spaces.   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a block with leading spaces.",
                "And this one has trailing spaces."
            ]
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_to_block_type_heading_multiple_hashes(self):
        block = "### This is a subheading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_to_block_type_code(self):
        block = "```\nThis is a code block\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_block_to_block_type_quote(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        
    def test_block_to_block_type_unordered_list(self):
        block = "- This is a list item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_ordered_list(self):
        block = "1. This is a list item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_block_to_block_type_paragraph(self):
        block = "This is a simple paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_misleading(self):
        block = "This check list - item is not a list."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_lists(self):
        md = """
- This is a list
- with items
- and _more_ items
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul></div>",
        )

    def test_ordered_lists(self):
        md = """
1. This is an ordered list
2. with items
3. and more items
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an ordered list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a blockquote block

this is paragraph text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )


    def test_all_blocks(self):
        md = """
# Heading Level 1

This is a paragraph with **bold** text and _italic_ text.

- Unordered item 1
- Unordered item 2

1. Ordered item 1
2. Ordered item 2

> This is a blockquote

```
print("Hello World")
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading Level 1</h1><p>This is a paragraph with <b>bold</b> text and <i>italic</i> text.</p><ul><li>Unordered item 1</li><li>Unordered item 2</li></ul><ol><li>Ordered item 1</li><li>Ordered item 2</li></ol><blockquote>This is a blockquote</blockquote><pre><code>print(\"Hello World\")\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()