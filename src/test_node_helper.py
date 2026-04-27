import unittest
from node_helper import split_nodes_delimiter, extract_markdown_images, split_nodes_image, split_nodes_link
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_images_ignores_non_text_nodes(self):
        node = TextNode("![image](https://example.com/image.png)", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_with_trailing_text(self):
        node = TextNode(
            "[home](https://example.com) is the homepage",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("home", TextType.LINK, "https://example.com"),
                TextNode(" is the homepage", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_does_not_parse_images(self):
        node = TextNode(
            "This is an image ![alt](https://example.com/image.png), not a link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)


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
