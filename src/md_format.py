import re
from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_parent = ParentNode("div", [], [])

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
            html_parent.children.append(ParentNode("p", text_to_child_nodes(block)))

        if block_type == BlockType.HEADING:
            h_count = len(block) - len(block.lstrip("#"))
            filtered_text = block.lstrip("# ")
            html_parent.children.append(
                ParentNode(f"h{h_count}", text_to_child_nodes(filtered_text))
            )

        if block_type == BlockType.CODE:
            filtered_block = block.lstrip("```\n").rstrip("```")
            code_node = LeafNode("code", filtered_block)
            html_parent.children.append(ParentNode("pre", [code_node]))

        if block_type == BlockType.QUOTE:
            filtered_block = block.lstrip("> ").rstrip("\n")
            html_parent.children.append(
                ParentNode("blockquote", text_to_child_nodes(filtered_block))
            )

        if block_type == BlockType.UNORDERED_LIST:
            list_items = block.split("\n")
            child_nodes = []
            for i in range(len(list_items)):
                text = list_items[i].split("- ", 1)[1]
                child_nodes.append(ParentNode("li", text_to_child_nodes(text)))

            html_parent.children.append(ParentNode("ul", child_nodes))

        if block_type == BlockType.ORDERED_LIST:
            list_items = block.split("\n")
            child_nodes = []
            for i in range(len(list_items)):
                text = list_items[i].split(". ", 1)[1]
                child_nodes.append(ParentNode("li", text_to_child_nodes(text)))

            html_parent.children.append(ParentNode("ol", child_nodes))

    return html_parent


def text_to_child_nodes(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception(
                f"Text doesn't contain enough delimiters.\nNode: {node}\nSplit text: {split_text}"
            )

        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                continue
            new_nodes.append(TextNode(split_text[i], text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        original_text = node.text
        sections = extract_markdown_images(original_text)
        if len(sections) == 0:
            new_nodes.append(node)
            continue

        for section in sections:
            image_alt = section[0]
            image_link = section[1]
            split_text = original_text.split(f"![{image_alt}]({image_link})", 1)
            new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            original_text = split_text[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    if len(new_nodes) == 0:
        raise Exception(f"Could not split image nodes.\nOld Nodes: {old_nodes}")
    for node in new_nodes:
        if node.text == "":
            new_nodes.remove(node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        original_text = node.text
        sections = extract_markdown_links(original_text)
        if len(sections) == 0:
            new_nodes.append(node)
            continue

        for section in sections:
            link_text = section[0]
            link = section[1]
            split_text = original_text.split(f"[{link_text}]({link})", 1)
            new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link))
            original_text = split_text[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    for node in new_nodes:
        if node.text == "":
            new_nodes.remove(node)
    return new_nodes


def text_to_textnodes(text):
    new_nodes = split_nodes_image(split_nodes_link([TextNode(text, TextType.TEXT)]))
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)

    return new_nodes


def markdown_to_blocks(text):
    md_blocks = text.split("\n\n")
    filtered_blocks = []
    for block in md_blocks:
        block = block.strip()
        if block == "":
            continue
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(md_block):
    if md_block.startswith("#"):
        return BlockType.HEADING
    if md_block.startswith("```"):
        return BlockType.CODE
    if md_block.startswith(">"):
        return BlockType.QUOTE
    if md_block.startswith("- "):
        return BlockType.UNORDERED_LIST
    if md_block.startswith("1. "):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_title(markdown: str) -> str:
    title_match = re.search(r"^# (.*)$", markdown, re.MULTILINE)
    if title_match:
        return title_match.group(1)
    raise Exception(f"Title could not be found in markdown: {markdown}")
