import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


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
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

class TestTextNodeSplit(unittest.TestCase):

    def test_split_nodes_delimiter(self):
        old_nodes = TextNode("This is a text node", TextType.NORMAL_TEXT)
        delimiter = " "
        text_type = TextType.NORMAL_TEXT
        new_nodes = split_nodes_delimiter([old_nodes], delimiter, text_type)
        self.assertEqual(new_nodes, 
                         [
                TextNode("This", TextType.NORMAL_TEXT),
                TextNode("is", TextType.NORMAL_TEXT),
                TextNode("a", TextType.NORMAL_TEXT),
                TextNode("text", TextType.NORMAL_TEXT),
                TextNode("node", TextType.NORMAL_TEXT),
            ]
        )

    def test_split_nodes_into_italic(self):
        old_nodes = TextNode("This is an _italic_ text node", TextType.NORMAL_TEXT)
        delimiter = "_"
        text_type = TextType.ITALIC_TEXT
        new_nodes = split_nodes_delimiter([old_nodes], delimiter, text_type)
        self.assertEqual(new_nodes, 
                         [
                TextNode("This is an ", TextType.NORMAL_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" text node", TextType.NORMAL_TEXT),
            ]
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC_TEXT)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD_TEXT),
                TextNode(" and ", TextType.NORMAL_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
            ],
            new_nodes
        )

    def test_split_nodes_invalid_syntax(self):
        old_nodes = TextNode("This is a _ text node", TextType.NORMAL_TEXT)
        delimiter = "_"
        text_type = TextType.ITALIC_TEXT
        with self.assertRaises(ValueError):
            split_nodes_delimiter([old_nodes], delimiter, text_type)

    def test_split_multiple_nodes(self):
        old_nodes = [
            TextNode("This is a text node", TextType.NORMAL_TEXT),
            TextNode("This is another text node", TextType.NORMAL_TEXT),
        ]
        delimiter = " "
        text_type = TextType.NORMAL_TEXT
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(new_nodes, 
                         [
                TextNode("This", TextType.NORMAL_TEXT),
                TextNode("is", TextType.NORMAL_TEXT),
                TextNode("a", TextType.NORMAL_TEXT),
                TextNode("text", TextType.NORMAL_TEXT),
                TextNode("node", TextType.NORMAL_TEXT),
                TextNode("This", TextType.NORMAL_TEXT),
                TextNode("is", TextType.NORMAL_TEXT),
                TextNode("another", TextType.NORMAL_TEXT),
                TextNode("text", TextType.NORMAL_TEXT),
                TextNode("node", TextType.NORMAL_TEXT),
            ]
        )