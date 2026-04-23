import unittest

from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "This is a text node", [], {"class": "title"})
        node2 = HTMLNode("h1", "This is a text node", [], {"class": "title"})
        self.assertEqual(node, node2)
    
    def test_not_eq_when_different_text(self):
        node = HTMLNode("h1", "This is a text node", [], {"class": "title"})
        node2 = HTMLNode("h1", "This is a different text node", [], {"class": "title"})
        self.assertNotEqual(node, node2)
    
    def test_not_eq_when_different_text_type(self):
        node = HTMLNode("h1", "This is a text node", [], {"class": "title"})
        node2 = HTMLNode("h1", "This is a text node", [], {"class": "subtitle"})
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()