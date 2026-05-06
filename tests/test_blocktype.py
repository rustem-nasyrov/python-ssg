import unittest
from src.blocktype import block_to_block_type, BlockType


class TestBlockType(unittest.TestCase):
    def test_heading_block(self):
        headings = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6",
        ]
        for heading in headings:
            block_type = block_to_block_type(heading)
            self.assertEqual(block_type, BlockType.HEADING)

    def test_code_block(self):
        code = """
```
def my_logger(value):
    print(f"My Logger: {value}"
```
"""
        block_type = block_to_block_type(code)
        self.assertEqual(block_type, BlockType.CODE)

    def test_paragraph_block(self):
        text = "Lorem ipsum"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_quote_block(self):
        quote = """> This is a quote
> This is still a quote
> And this is also a quote"""
        block_type = block_to_block_type(quote)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_unordered_list_block(self):
        unordered_list = """- First item
- Second item
- Third item"""
        block_type = block_to_block_type(unordered_list)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        ordered_list = """1. First item
2. Second item
3. Third item"""
        block_type = block_to_block_type(ordered_list)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_invalid_heading_with_too_many_hashes_is_paragraph(self):
        text = "####### This is not a valid heading"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
