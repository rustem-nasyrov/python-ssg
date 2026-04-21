import re

from textnode import TextNode, TextType
from htmlnode import LeafNode


def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode('b', text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode('i', text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode('code', text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode('a', text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode('img', text_node.text, {"src": text_node.url})
    return ""


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res = []
    delimiter_len = len(delimiter)

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            res.append(node)
            continue

        text = node.text

        while len(text) > 0:
            start = text.find(delimiter, 0)
            if start == -1:
                res.append(TextNode(text, TextType.TEXT))
                break
            end = text.find(delimiter, start + delimiter_len)
            if end == -1:
                raise ValueError("Could not find end delimiter")
            head = text[:start]
            if len(head) > 0:
                res.append(TextNode(head, TextType.TEXT))
            res.append(TextNode(text[start + delimiter_len:end], text_type))
            text = text[end + delimiter_len:]
    return res


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
