class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list | None = None,
        props: dict | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join([f'{k}="{v}"' for k, v in self.props.items()])

    def __repr__(self):
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"


class LeafNode(HTMLNode):
    def __init__(self, value: str, tag: str | None = None, props: dict | None = None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __eq__(self, other) -> bool:
        return (
            self.value == other.value
            and self.tag == other.tag
            and self.props == other.props
        )


class ParentNode(HTMLNode):
    def __init__(
        self,
        children: list,
        tag: str | None = None,
        props: dict | None = None,
    ):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Missing tag")
        if not self.children:
            raise ValueError("Missing children")

        html = f"<{self.tag}{self.props_to_html()}>"
        for node in self.children:
            html += node.to_html()
        html += f"</{self.tag}>"

        return html
