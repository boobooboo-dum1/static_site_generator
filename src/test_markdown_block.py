import unittest
from textwrap import dedent

from markdown_block import block_to_block_type, markdown_to_blocks


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

    def test_block_to_block_type_heading(self):
        text = "# This is a heading"
        result = block_to_block_type(text)
        expected = "heading"
        self.assertEqual(result, expected)

    def test_block_to_block_type_code(self):
        text = "``` This is a code block \n\
            with multiples lines \n\
            ```"
        result = block_to_block_type(text)
        expected = "code"
        self.assertEqual(result, expected)

    def test_block_to_block_type_quote(self):
        text = dedent(
            """
            >This is a quote block
            > with multiples lines
            >and more multiples lines"""
        ).strip()
        result = block_to_block_type(text)
        expected = "quote"
        self.assertEqual(result, expected)

    def test_block_to_block_type_unordered_list(self):
        text = dedent(
            """
            - This is a unorder list
            * with multiples lines
            * and more multiples lines"""
        ).strip()
        result = block_to_block_type(text)
        expected = "unordered_list"
        self.assertEqual(result, expected)

    def test_block_to_block_type_ordered_list(self):
        text = dedent(
            """
            1. This is an ordered list
            2. with multiples lines
            3. and more multiples lines"""
        ).strip()

        result = block_to_block_type(text)
        expected = "ordered_list"
        self.assertEqual(result, expected)

    def test_block_to_block_type_other_ordered_list(self):
        text = dedent(
            """
            2. This is an ordered list
            3. with multiples lines
            4. and more multiples lines"""
        ).strip()

        result = block_to_block_type(text)
        expected = "ordered_list"
        self.assertEqual(result, expected)

    def test_block_to_block_type_flase_ordered_list(self):
        text = dedent(
            """
            2. This is an ordered list
            1. with multiples lines
            4. and more multiples lines"""
        ).strip()

        result = block_to_block_type(text)
        expected = "paragraph"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
