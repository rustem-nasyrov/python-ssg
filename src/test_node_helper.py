import unittest
from node_helper import split_nodes_delimiter, extract_markdown_images
from src.node_helper import extract_markdown_links
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

    def test_split_two(self):
        node = TextNode("This is _text_ with a italic phrase _in the end_", TextType.TEXT)
        outcome = split_nodes_delimiter([node], "_", TextType.ITALIC)
        target = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.ITALIC),
            TextNode(" with a italic phrase ", TextType.TEXT),
            TextNode("in the end", TextType.ITALIC),
        ]
        self.assertEqual(outcome, target)


class TestExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
