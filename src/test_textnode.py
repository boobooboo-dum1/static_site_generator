import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "my url")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        result = str(TextNode("This is a text node", TextType.BOLD))
        expected = "TextNode(This is a text node, bold, None)"
        self.assertEqual(result, expected)


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        text_node = TextNode(text="Normal text", text_type=TextType.TEXT)
        result = text_node_to_html_node(text_node)
        expected_node = LeafNode(value="Normal text")
        self.assertEqual(result, expected_node)

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode(text="Bold text", text_type=TextType.BOLD)
        result = text_node_to_html_node(text_node)
        expected_node = LeafNode(value="Bold text", tag="b")
        self.assertEqual(result, expected_node)

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode(text="Italic text", text_type=TextType.ITALIC)
        result = text_node_to_html_node(text_node)
        expected_node = LeafNode(value="Italic text", tag="i")
        self.assertEqual(result, expected_node)

    def test_text_node_to_html_node_link(self):
        text_node = TextNode(
            text="Link text", text_type=TextType.LINK, url="www.test.com"
        )
        result = text_node_to_html_node(text_node)
        expected_node = LeafNode(
            value="Link text", tag="a", props={"href": "www.test.com"}
        )
        self.assertEqual(result, expected_node)

    def test_text_node_to_html_node_img(self):
        text_node = TextNode(
            text="Image alt text", text_type=TextType.IMAGE, url="www.test.com"
        )
        result = text_node_to_html_node(text_node)
        expected_node = LeafNode(
            value="", tag="img", props={"src": "www.test.com", "alt": "Image alt text"}
        )
        self.assertEqual(result, expected_node)

    def test_text_node_to_html_node_not_text_type(self):
        class SomeOtherType:
            value = "Other value"

        _ = TextNode(
            text="Image alt text",
            text_type=SomeOtherType(),  # type: ignore
            url="www.test.com",
        )
        self.assertRaises(ValueError)


if __name__ == "__main__":
    unittest.main()
