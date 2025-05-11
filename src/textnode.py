from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    NORMAL_TEXT = 0
    BOLD_TEXT = 1
    ITALIC_TEXT = 2
    CODE_TEXT = 3
    LINKS = 4
    IMAGE = 5

class TextNode:
    def __init__(self, text: str, text_type: TextType, URL: str = None):
        self.text = text
        self.text_type = text_type
        self.URL = URL
    
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.URL == other.URL)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.URL})"
    
def text_node_to_html_node(text_node):
    """
    Convert a TextNode to an HTMLNode.
    """
    if text_node.text_type == TextType.NORMAL_TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD_TEXT:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC_TEXT:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE_TEXT:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINKS:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.URL})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src": text_node.URL, "alt": text_node.text})