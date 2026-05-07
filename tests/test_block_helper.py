import unittest
from src.block_helper import (markdown_to_blocks, markdown_to_html_node, extract_title)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_trims_outer_whitespace(self):
        md = """

    First block with leading spaces    

    Second block with trailing spaces    

        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block with leading spaces",
                "Second block with trailing spaces",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "Just one paragraph with no blank lines"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Just one paragraph with no blank lines",
            ],
        )

    def test_markdown_to_blocks_preserves_single_newlines_inside_block(self):
        md = """
Line one
Line two
Line three
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Line one\nLine two\nLine three",
            ],
        )

    def test_markdown_to_blocks_multiple_blank_lines_create_empty_blocks(self):
        md = """
First block



Second block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block",
                "",
                "Second block",
            ],
        )

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [""])

    def test_markdown_to_blocks_whitespace_only_string(self):
        md = "     \n\n     "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [""])

    def test_markdown_to_blocks_keeps_indentation_inside_block(self):
        md = """
Paragraph:
    indented line
    another indented line

Next block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Paragraph:\n    indented line\n    another indented line",
                "Next block",
            ],
        )


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello, World!"
        self.assertEqual("Hello, World!", extract_title(md))

    def test_title_in_the_middle(self):
        md = """
Lorem ipsum
# Hello, World!
Foo
Bar
"""
        self.assertEqual("Hello, World!", extract_title(md))

    def test_no_title(self):
        with self.assertRaises(Exception):
            extract_title("")
