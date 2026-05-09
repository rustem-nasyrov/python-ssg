import re

from src.blocktype import block_to_block_type, BlockType
from src.htmlnode import ParentNode
from src.node_helper import text_to_textnodes, text_node_to_html_node
from src.textnode import TextNode, TextType


def markdown_to_blocks(markdown):
    rows = markdown.strip().split("\n\n")

    filter(lambda s: len(s) > 0, rows)

    for i in range(0, len(rows)):
        rows[i] = rows[i].strip()

    return rows


def _text_to_children(text: str):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(n) for n in text_nodes]


def _paragraph_block(block: str) -> ParentNode:
    text = " ".join(block.splitlines())
    return ParentNode("p", _text_to_children(text))


def _code_block(block: str) -> ParentNode:
    lines = block.splitlines(True)

    first = next((i for i, l in enumerate(lines) if l.strip() == "```"), None)
    last = None
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() == "```":
            last = i
            break

    inner = "".join(lines[(first + 1) if first is not None else 0: last])

    code_leaf = text_node_to_html_node(TextNode(inner, TextType.CODE))
    return ParentNode("pre", [code_leaf])


def _heading_block(block: str) -> ParentNode:
    m = re.match(r"^(#{1,6})\s*(.*)$", block)
    level = len(m.group(1))
    text = m.group(2).strip()
    return ParentNode(f"h{level}", _text_to_children(text))


def _quote_block(block: str) -> ParentNode:
    lines = [re.sub(r"^>\s?", "", l) for l in block.splitlines()]
    text = " ".join(lines)
    return ParentNode("blockquote", _text_to_children(text))


def _ul_block(block: str) -> ParentNode:
    items = []
    for line in block.splitlines():
        item_text = re.sub(r"^-\s", "", line)
        items.append(ParentNode("li", _text_to_children(item_text)))
    return ParentNode("ul", items)


def _ol_block(block: str) -> ParentNode:
    items = []
    for line in block.splitlines():
        item_text = re.sub(r"^\d+\.\s", "", line)
        items.append(ParentNode("li", _text_to_children(item_text)))
    return ParentNode("ol", items)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        if block == "":
            continue

        btype = block_to_block_type(block)

        if btype == BlockType.PARAGRAPH:
            children.append(_paragraph_block(block))
        elif btype == BlockType.CODE:
            children.append(_code_block(block))
        elif btype == BlockType.HEADING:
            children.append(_heading_block(block))
        elif btype == BlockType.QUOTE:
            children.append(_quote_block(block))
        elif btype == BlockType.UNORDERED_LIST:
            children.append(_ul_block(block))
        elif btype == BlockType.ORDERED_LIST:
            children.append(_ol_block(block))
        else:
            children.append(_paragraph_block(block))

    return ParentNode("div", children)


def extract_title(markdown):
    title_match = re.search(r"^#(?!#)\s+(.+)$", markdown, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()
    raise Exception("Title not found")
