import unittest
from textwrap import dedent

from htmlnode import LeafNode, ParentNode
from markdown_to_html import markdown_to_html_node, text_to_children


class TestMarkdownToHtm(unittest.TestCase):
    def test_text_to_children(self):
        text = dedent(
            """
            *This is a italic line*
            And a line
            and another with **bold**"""
        ).strip()
        result = text_to_children(text)

        expected = [
            LeafNode(value="This is a italic line", tag="i"),
            LeafNode(value="And a line"),
            LeafNode(value="and another with "),
            LeafNode(value="bold", tag="b"),
        ]
        self.assertEqual(result, expected)

    def test_markdown_to_html_node_paragraph(self):
        text = dedent(
            """
            *This is a italic line*
            And a line
            and another with **bold**"""
        ).strip()
        result = markdown_to_html_node(text)

        expected_children = [
            LeafNode(value="This is a italic line", tag="i"),
            LeafNode(value="And a line"),
            LeafNode(value="and another with "),
            LeafNode(value="bold", tag="b"),
        ]
        expected_block = ParentNode(children=expected_children, tag="p")
        expected = ParentNode(children=[expected_block], tag="div")

        self.assertEqual(result, expected)

    def test_markdown_to_html_node_code(self):
        text = dedent(
            """
            ```This is a
            block code
            on multiple lines```"""
        ).strip()
        result = markdown_to_html_node(text)

        expected_children = [
            LeafNode(
                value="This is a\nblock code\non multiple lines", tag="blockquote"
            ),
        ]
        expected = ParentNode(children=expected_children, tag="div")

        self.assertEqual(result, expected)
