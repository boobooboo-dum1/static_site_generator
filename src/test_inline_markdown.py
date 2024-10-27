import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertListEqual(result, expected)

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold text** word", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertListEqual(result, expected)

    def test_split_nodes_delimiter_no_bold(self):
        node = TextNode("This is text with a without bold text word", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This is text with a without bold text word", TextType.TEXT),
        ]

        self.assertListEqual(result, expected)

    def test_split_nodes_delimiter_multiple_bold(self):
        node = TextNode(
            "This is text with a **bold text** and **other bold text**", TextType.TEXT
        )
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("other bold text", TextType.BOLD),
        ]

        self.assertListEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
