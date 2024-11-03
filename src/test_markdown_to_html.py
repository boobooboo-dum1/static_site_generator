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
            LeafNode(value=" And a line and another with "),
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
            ParentNode(
                children=[
                    LeafNode(
                        value="This is a\nblock code\non multiple lines", tag="code"
                    )
                ],
                tag="pre",
            ),
        ]
        expected = ParentNode(children=expected_children, tag="div")

        self.assertEqual(result, expected)

    def test_markdown_to_html_node_headings(self):
        text = dedent(
            """
            # My heading 1

            ## My heading 2

            ### My heading 3

            #### My heading 4

            ##### My heading 5

            ###### My heading 6"""
        ).strip()
        result = markdown_to_html_node(text)

        expected_children = [
            ParentNode(children=[LeafNode(value="My heading 1")], tag="h1"),
            ParentNode(children=[LeafNode(value="My heading 2")], tag="h2"),
            ParentNode(children=[LeafNode(value="My heading 3")], tag="h3"),
            ParentNode(children=[LeafNode(value="My heading 4")], tag="h4"),
            ParentNode(children=[LeafNode(value="My heading 5")], tag="h5"),
            ParentNode(children=[LeafNode(value="My heading 6")], tag="h6"),
        ]
        expected = ParentNode(children=expected_children, tag="div")

        self.assertEqual(result, expected)

    def test_markdown_to_html_node_quote(self):
        text = dedent(
            """
            > This is a
            > quote text
            > on multiple lines"""
        ).strip()
        result = markdown_to_html_node(text)

        expected_children = [
            LeafNode(value="This is a quote text on multiple lines", tag="blockquote")
        ]
        expected = ParentNode(children=expected_children, tag="div")

        self.assertEqual(result, expected)

    def test_markdown_to_html_node_unordered_list(self):
        text = dedent(
            """
            * This is a
            * unordered list
            * with multiple
            * items"""
        ).strip()
        result = markdown_to_html_node(text)

        expected_subchildren = [
            ParentNode(children=[LeafNode(value="This is a")], tag="li"),
            ParentNode(children=[LeafNode(value="unordered list")], tag="li"),
            ParentNode(children=[LeafNode(value="with multiple")], tag="li"),
            ParentNode(children=[LeafNode(value="items")], tag="li"),
        ]
        expected_children = [ParentNode(children=expected_subchildren, tag="ul")]
        expected = ParentNode(children=expected_children, tag="div")

        self.assertEqual(result, expected)

    def test_markdown_to_html_node_ordered_list(self):
        text = dedent(
            """
            1. This is a
            2. ordered list
            3. with multiple
            4. items"""
        ).strip()
        result = markdown_to_html_node(text)

        expected_subchildren = [
            ParentNode(children=[LeafNode(value="This is a")], tag="li"),
            ParentNode(children=[LeafNode(value="ordered list")], tag="li"),
            ParentNode(children=[LeafNode(value="with multiple")], tag="li"),
            ParentNode(children=[LeafNode(value="items")], tag="li"),
        ]
        expected_children = [ParentNode(children=expected_subchildren, tag="ol")]
        expected = ParentNode(children=expected_children, tag="div")

        self.assertEqual(result, expected)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
