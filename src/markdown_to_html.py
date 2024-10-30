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
                children = text_to_children(block)
                nodes.append(ParentNode(children=children, tag="p"))
            case BlockType.CODE.value:
                nodes.append(LeafNode(value=block[3:-3], tag="blockquote"))

    return ParentNode(children=nodes, tag="div")


def text_to_children(text: str) -> list[HTMLNode]:
    lines = text.split("\n")
    nodes = []
    for line in lines:
        text_nodes = text_to_textnodes(line)
        nodes.extend([text_node_to_html_node(node) for node in text_nodes])
    return nodes
