import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
    
    def test_unequal(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a different text node", TextType.NORMAL_TEXT)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT, "https://example.com")
        expected_repr = "TextNode(This is a text node, 1, https://example.com)"
        self.assertEqual(repr(node), expected_repr)
    
    def test_repr_without_url(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        expected_repr = "TextNode(This is a text node, 1, None)"
        self.assertEqual(repr(node), expected_repr)

if __name__ == "__main__":
    unittest.main()

class TestTextNodeConversion(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")