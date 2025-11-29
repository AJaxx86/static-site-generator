from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        self.tag = tag
        self.children = children
        self.props = props
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError(f"ParentNode tag not assigned.")
        if self.children == [] or self.children == None:
            raise ValueError(f"ParentNode children not assigned.")
        return f"<{self.tag}>" + "".join(node.to_html() for node in self.children) + f"</{self.tag}>"