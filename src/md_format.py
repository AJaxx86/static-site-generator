from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        split_text = node.text.split(delimiter)
    
    new_nodes.extend(split_text)

split_nodes_delimiter([TextNode("Here's some **bold** text.", TextType.TEXT)], "**", TextType.BOLD)