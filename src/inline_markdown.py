import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            nodes.append(old_node)
            continue

        splitted = old_node.text.split(delimiter, maxsplit=2)

        # delimiter not found in string
        if len(splitted) == 1:
            if splitted[0]:
                nodes.append(TextNode(text=splitted[0], text_type=TextType.TEXT))
            continue

        if len(splitted) == 2:
            nodes.append(TextNode(text=splitted[0], text_type=TextType.TEXT))
            nodes.append(
                TextNode(text=delimiter + splitted[0], text_type=TextType.TEXT)
            )
            continue

        # delimiter found in string
        first, mid, last = splitted

        # fisrt part is not empty, meaning it do not match our separator
        # lets add it as a TEXT type
        if first:
            nodes.append(TextNode(text=first, text_type=TextType.TEXT))

        # mid part is always the part enclosed by separator
        nodes.append(TextNode(text=mid, text_type=text_type))

        if last:
            # Lets recurse for last part
            child_nodes = split_nodes_delimiter(
                [TextNode(text=last, text_type=TextType.TEXT)],
                delimiter=delimiter,
                text_type=text_type,
            )
            nodes.extend(child_nodes)

    return nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            nodes.append(TextNode(text=old_node.text, text_type=TextType.TEXT))
            continue

        alt, url = images[0]
        delimiter = f"![{alt}]({url})"
        splitted = old_node.text.split(delimiter, maxsplit=1)
        if len(splitted) == 1:
            raise ValueError("Fail to split node image")
        first, last = splitted

        # Image is not in first position in string
        if first != "":
            nodes.append(TextNode(text=first, text_type=TextType.TEXT))

        # Append image node
        nodes.append(TextNode(text=alt, url=url, text_type=TextType.IMAGE))

        # Nothing more to process
        if last == "":
            continue

        remaining_node = TextNode(text=last, text_type=TextType.TEXT)
        nodes.extend(split_nodes_image([remaining_node]))

    return nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            nodes.append(TextNode(text=old_node.text, text_type=TextType.TEXT))
            continue

        text, url = links[0]
        delimiter = f"[{text}]({url})"
        splitted = old_node.text.split(delimiter, maxsplit=1)
        if len(splitted) == 1:
            raise ValueError("Fail to split node link")
        first, last = splitted

        # Link is not in first position in string
        if first != "":
            nodes.append(TextNode(text=first, text_type=TextType.TEXT))

        # Append link node
        nodes.append(TextNode(text=text, url=url, text_type=TextType.LINK))

        # Nothing more to process
        if last == "":
            continue

        remaining_node = TextNode(text=last, text_type=TextType.TEXT)
        nodes.extend(split_nodes_link([remaining_node]))

    return nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    base_node = TextNode(text, text_type=TextType.TEXT)
    nodes = split_nodes_image([base_node])
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes
