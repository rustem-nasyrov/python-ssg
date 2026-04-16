import unittest
from node_helper import split_nodes_delimiter
from textnode import TextType, TextNode


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_start(self):
        node = TextNode("`This is text` with a code phrase in the start", TextType.TEXT)
        outcome = split_nodes_delimiter([node], "`", TextType.CODE)
        target = [
            TextNode("This is text", TextType.CODE),
            TextNode(" with a code phrase in the start", TextType.TEXT),
        ]
        self.assertEqual(outcome, target)

    def test_split_nodes_delimiter_middle(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        outcome = split_nodes_delimiter([node], "**", TextType.BOLD)
        target = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(outcome, target)

    def test_split_nodes_delimiter_end(self):
        node = TextNode("This is text with a italic phrase _in the end_", TextType.TEXT)
        outcome = split_nodes_delimiter([node], "_", TextType.ITALIC)
        target = [
            TextNode("This is text with a italic phrase ", TextType.TEXT),
            TextNode("in the end", TextType.ITALIC),
        ]
        self.assertEqual(outcome, target)
