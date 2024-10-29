import unittest
from textwrap import dedent

from block_markdown import markdown_to_blocks


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = dedent("""
            # This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is the first list item in a list block
            * This is a list item
            * This is another list item""")
        result = markdown_to_blocks(text)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            dedent("""
            * This is the first list item in a list block
            * This is a list item
            * This is another list item""").strip(),
        ]

        self.assertListEqual(result, expected)

    def test_markdown_to_blocks_extra_lines(self):
        text = dedent("""
            # This is a heading


            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            """)
        result = markdown_to_blocks(text)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
        ]

        self.assertListEqual(result, expected)
