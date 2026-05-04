from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(text):
    if re.search(r"^#{1,6}\s?\w", text):
        return BlockType.HEADING

    if re.search(r"^\n?```\n", text) and re.search(r"```\n?$", text):
        return BlockType.CODE

    text_lines = text.splitlines()

    if re.match(r">\s?", text):
        for line in text_lines:
            if not re.match(r">\s?", line):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if re.match(r"^-\s", text):
        for line in text_lines:
            if not re.match(r"^-\s", line):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if re.match(r"^\d+\.\s", text):
        for line in text_lines:
            if not re.match(r"^\d+\.\s", line):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
