import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("Code Node", TextType.CODE)
        node2 = TextNode("Link Node", TextType.LINK, "https://example.com/")
        self.assertNotEqual(node, node2)

    def test_link_eq(self):
        node = TextNode("Link Node", TextType.LINK, "https://example.com/")
        node2 = TextNode("Link Node", TextType.LINK, "https://example.com/")
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
