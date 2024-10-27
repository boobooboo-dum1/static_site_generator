from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type.value
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT.value:
            return LeafNode(value=text_node.text)
        case TextType.BOLD.value:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC.value:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE.value:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK.value:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE.value:
            return LeafNode(
                tag="img",
                value="",
                props={"src": text_node.url, "alt": text_node.text},
            )
        case _:
            raise ValueError(f"text_type should match on of {TextType} value")
