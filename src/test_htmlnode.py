import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode('div')
        node2 = HTMLNode('div')
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = HTMLNode(value="Foo")
        node2 = HTMLNode(value="Bar")
        self.assertNotEqual(node, node2)

    def test_eq_props(self):
        node = HTMLNode("link", props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        prop_str = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), prop_str)


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        leaf = LeafNode("p", "Lorem")
        leaf2 = LeafNode("p", "Lorem")
        self.assertEqual(leaf, leaf2)

    def test_not_eq_text(self):
        leaf = LeafNode(tag="span", value="Foo")
        leaf2 = LeafNode(tag="span", value="Bar")
        self.assertNotEqual(leaf, leaf2)

    def test_to_html(self):
        leaf_html = LeafNode(tag="p", value="Hello, World!").to_html()
        html_str = '<p>Hello, World!</p>'
        self.assertEqual(leaf_html, html_str)

    def test_no_tag(self):
        value = "Text"
        leaf_html = LeafNode(tag=None, value=value).to_html()
        self.assertEqual(leaf_html, value)
