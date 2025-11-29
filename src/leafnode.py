import textnode
from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        self.tag = tag
        self.value = value
        self.props = props
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError(f"LeafNode value not assigned.")
        if self.tag == None or self.tag == "":
            return self.value
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def text_node_to_html_node(self, text_node):
        if text_node.type not in textnode.TextType:
            raise Exception(f"Incorrect type assigned to text node: {text_node.type}")
        