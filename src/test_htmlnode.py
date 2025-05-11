import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode(tag="div", value={"class": "container"}, children=[], props={"id": "main"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, {"class": "container"})
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"id": "main"})

    def test_props_to_html(self):
        node = HTMLNode(props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), 'class="container" id="main"')

    def test_repr(self):
        node = HTMLNode(tag="div", value={"class": "container"}, children=[], props={"id": "main"})
        expected_repr = "HTMLNode(tag=div, value={'class': 'container'}, children=[], props={'id': 'main'})"
        self.assertEqual(repr(node), expected_repr)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    

    def test_leaf_repr(self):
        node = LeafNode(tag="p", value="Hello, world!", props={"class": "text"})
        expected_repr = "LeafNode(tag=p, value=Hello, world!, children=[], props={'class': 'text'})"
        self.assertEqual(repr(node), expected_repr)
    
    def test_leaf_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="p", value=None)

    
    """
    Skipping this one, since leaf code values cannot be empty
    def test_leaf_img(self):
        img_node = LeafNode("img", "", {"src": "example.jpg", "alt": "Example image"})
        self.assertEqual(img_node.to_html(), '<img src="example.jpg" alt="Example image"></img>')
    """

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_repr(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(tag="div", children=[child_node], props={"class": "container"})
        expected_repr = "HTMLNode(tag=div, value={}, children=[LeafNode(tag=span, value=child, children=[], props={})], props={'class': 'container'})"
        self.assertEqual(repr(parent_node), expected_repr)