import unittest
from htmlnode import HTMLNode


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
