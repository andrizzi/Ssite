class HTMLNode:
    """
    A class representing an HTML node.
    """

    def __init__(self, tag: str = None, value: dict = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value if value else {}
        self.children = children if children else []
        self.props = props if props else {}

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method.")
    
    def props_to_html(self):
        """
        Convert the properties of the node to an HTML string.
        :return: A string representation of the properties in HTML format.
        """
        if self.props is None:
            return ""
        result = " ".join([f'{key}="{value}"' for key, value in self.props.items()])
        if result and self.tag:
            return " " + result
        else:
            return result

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    """
    a child class of HTMLNode called LeafNode. Its constructor should differ slightly from the HTMLNode class because:
    It should not allow for any children
    The value data member should be required (and tag even though the tag's value may be None)
    """

#Use the super() function to call the constructor of the HTMLNode class.
    def __init__(self, tag: str, value: dict, props: dict = None):
        if not value:
            raise ValueError("Value is required for LeafNode.")
        if not tag and tag is not None:
            raise ValueError("Tag is required for LeafNode.")
        super().__init__(tag=tag, value=value, children=[], props=props)
        # Ensure that LeafNode does not have children

    """
    Add a .to_html() method that renders a leaf node as an HTML string (by returning a string).
    If the leaf node has no value, it should raise a ValueError. All leaf nodes must have a value.
    If there is no tag (e.g. it's None), the value should be returned as raw text.
    Otherwise, it should render an HTML tag. For example, these leaf nodes:
    """

    def to_html(self):
        """
        Convert the LeafNode to an HTML string.

        :return: A string representation of the LeafNode in HTML format.
        """
        if not self.value:
            raise ValueError("LeafNode must have a value.")
        if not self.tag:
            return str(self.value)
        else:
            props_str = self.props_to_html()
            return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, children=[], props={self.props})"
    
    """
    Any HTML node that's not "leaf" node (i.e. it has children) is a "parent" node.
    """
class ParentNode(HTMLNode):
    """
    The tag and children arguments are not optional
It doesn't take a value argument
props is optional
(It's the exact opposite of the LeafNode class)"""

    def __init__(self, tag: str, children: list, props: dict = None):
        if not tag:
            raise ValueError("Tag is required for ParentNode.")
        super().__init__(tag=tag, value={}, children=children, props=props)

    def to_html(self):

        if self.tag is None:
            raise ValueError("Tag is required for ParentNode.")
        if not self.children:
            raise ValueError("ParentNode must have children.")
        #return a string representing the HTML tag of the node and its children
        return f"<{self.tag}{self.props_to_html()}>" + "".join([child.to_html() for child in self.children]) + f"</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"