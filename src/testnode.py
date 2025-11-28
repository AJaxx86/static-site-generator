from enum import Enum

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.type = TextType(text_type).value
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.type == other.type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.type}, {self.url})"