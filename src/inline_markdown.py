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
