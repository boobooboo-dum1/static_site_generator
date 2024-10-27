import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )

        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(expected, node.props_to_html())

    def test_props_to_html_no_props(self):
        node = HTMLNode()

        expected = ""
        self.assertEqual(expected, node.props_to_html())

    def test_repr(self):
        node = HTMLNode(
            tag="a",
            value="my_value",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        expected = 'HTMLNode(a, my_value, None,  href="https://www.google.com" target="_blank")'
        self.assertEqual(expected, str(node))


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(
            tag="a", value="Click me!", props={"href": "https://www.google.com"}
        )

        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(expected, node.to_html())

    def test_to_html_no_props(self):
        node = LeafNode(tag="p", value="This is a paragraph of text.")

        expected = "<p>This is a paragraph of text.</p>"
        self.assertEqual(expected, node.to_html())


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            tag="p",
            children=[
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(expected, node.to_html())

    def test_to_html_with_parent(self):
        node = ParentNode(
            tag="p",
            children=[
                ParentNode(
                    tag="i",
                    children=[
                        LeafNode(tag="b", value="Bold text"),
                        LeafNode(tag=None, value="Normal text"),
                    ],
                ),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
        )
        expected = (
            "<p><i><b>Bold text</b>Normal text</i><i>italic text</i>Normal text</p>"
        )
        self.assertEqual(expected, node.to_html())

    def test_to_html_with_children(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode(tag="span", children=[grandchild_node])
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_headings(self):
        node = ParentNode(
            tag="h2",
            children=[
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
