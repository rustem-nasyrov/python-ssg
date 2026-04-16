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
        start = None
        end = None
        for i in range(0, len(text)):
            if text[i:i + delimiter_len] == delimiter:
                if start is None:
                    start = i
                elif end is None:
                    end = i
        if end is None:
            raise Exception(f"Could not find matching delimiter")
        if start == 0:
            res.append(TextNode(text[start + delimiter_len:end], text_type))
            res.append(TextNode(text[end + delimiter_len:], TextType.TEXT))
        elif start > 0 and end + delimiter_len == len(text):
            res.append(TextNode(text[0:start], TextType.TEXT))
            res.append(TextNode(text[start + delimiter_len:end], text_type))
        else:
            res.append(TextNode(text[0:start], TextType.TEXT))
            res.append(TextNode(text[start + delimiter_len:end], text_type))
            res.append(TextNode(text[end + delimiter_len:], TextType.TEXT))
    return res
