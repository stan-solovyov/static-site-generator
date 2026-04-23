import unittest

from helpers.helper_functions import split_nodes_delimiter, split_nodes_delimiter, text_node_to_html_node
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq_when_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_when_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold text node")
    
    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is an italic text node")
        
    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a code text node")
    
    def test_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props['href'], "https://example.com")
    
    def test_split_nodes_delimiter(self):
        nodes = [TextNode("This is a text node", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, " ", TextType.TEXT)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This")
        self.assertEqual(new_nodes[1].text, "is")
        self.assertEqual(new_nodes[2].text, "a")
        self.assertEqual(new_nodes[3].text, "text")
        self.assertEqual(new_nodes[4].text, "node")
    
    def test_split_nodes_delimiter_with_non_matching_type(self):
        nodes = [TextNode("This is a text node", TextType.BOLD)]
        new_nodes = split_nodes_delimiter(nodes, " ", TextType.TEXT)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is a text node")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
    
    def test_split_nodes_delimiter_with_invalid_syntax(self):
        nodes = [TextNode("Thisisatext node", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, " ", TextType.TEXT)

if __name__ == "__main__":
    unittest.main()