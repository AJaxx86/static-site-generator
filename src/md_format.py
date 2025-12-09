import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception(f"Text doesn't contain enough delimiters.\nNode: {node}\nSplit text: {split_text}")

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
        for section in sections:
            image_alt = section[0]
            image_link = section[1]
            split_text = original_text.split(f"![{image_alt}]({image_link})", 1)
            new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            original_text = split_text[1]

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        original_text = node.text
        sections = extract_markdown_links(original_text)
        for section in sections:
            link_text = section[0]
            link = section[1]
            split_text = original_text.split(f"[{link_text}]({link})", 1)
            new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link))
            original_text = split_text[1]

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
