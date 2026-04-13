class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError(self)

    def props_to_html(self):
        if self.props is None:
            return ""
        props_list = []

        for key in self.props:
            props_list.append(f'{key}="{self.props[key]}"')

        return " ".join(props_list).strip()

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value is None or self.value == "":
            raise ValueError()
        if self.tag is None or self.tag == "":
            return self.value
        props = " " + self.props_to_html() if self.props else ""
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.props == other.props

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("The tag is required")
        if self.children is None:
            raise ValueError("The children are required")
        children_list = []
        for child in self.children:
            children_list.append(child.to_html())
        props = " " + self.props_to_html() if self.props else ""
        return f"<{self.tag}{props}>{''.join(children_list)}</{self.tag}>"
