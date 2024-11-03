from typing import Literal

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from markdown_block import BlockType, block_to_block_type, markdown_to_blocks
from textnode import text_node_to_html_node


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.PARAGRAPH.value:
                paragraph_text = " ".join([line for line in block.split("\n")])
                children = text_to_children(paragraph_text)
                nodes.append(ParentNode(children=children, tag="p"))
            case BlockType.CODE.value:
                nodes.append(
                    ParentNode(
                        children=[LeafNode(value=block[3:-3], tag="code")], tag="pre"
                    )
                )
            case BlockType.HEADING.value:
                heading_char, content = block.split(" ", maxsplit=1)
                children = text_to_children(content)
                nodes.append(ParentNode(children=children, tag=f"h{len(heading_char)}"))
            case BlockType.QUOTE.value:
                quote_text = " ".join(
                    [skip_start_characters(line, 1) for line in block.split("\n")]
                )
                nodes.append(LeafNode(value=quote_text, tag="blockquote"))
            case BlockType.UNORDERED_LIST.value:
                nodes.append(mardown_list_to_hmtl_node(block, "unordered"))
            case BlockType.ORDERED_LIST.value:
                nodes.append(mardown_list_to_hmtl_node(block, "ordered"))
            case _:
                raise ValueError("Fail to convert mardown to html")

    return ParentNode(children=nodes, tag="div")


def text_to_children(text: str) -> list[HTMLNode]:
    lines = text.split("\n")
    nodes = []
    for line in lines:
        text_nodes = text_to_textnodes(line)
        nodes.extend([text_node_to_html_node(node) for node in text_nodes])
    return nodes


def skip_start_characters(text: str, skipped: int) -> str:
    lines = text.split("\n")

    return "\n".join([line[skipped:].strip() for line in lines])


def mardown_list_to_hmtl_node(
    mardown: str, list_type: Literal["unordered", "ordered"]
) -> HTMLNode:
    if list_type == "unordered":
        skipped = 2
    else:
        skipped = 3

    lines = mardown.split("\n")
    list_node = []
    for line in lines:
        content = skip_start_characters(line, skipped)
        children = text_to_children(content)

        list_node.append(ParentNode(children=children, tag="li"))

    if list_type == "unordered":
        return ParentNode(children=list_node, tag="ul")
    return ParentNode(children=list_node, tag="ol")
