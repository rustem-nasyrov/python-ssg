self_closing_tags = ["img"]


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError(self)

    def is_self_closing(self):
        return self.tag.lower() in self_closing_tags

    def get_props(self):
        props = self.props

        if self.is_self_closing() and "alt" not in props:
            props["alt"] = self.value

        return props

    def props_to_html(self):
        props = self.get_props()

        if props is None:
            return ""

        props_list = []

        for key in props:
            props_list.append(f'{key}="{props[key]}"')

        return " ".join(props_list).strip()

    def __eq__(self, other: HTMLNode):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.get_props() == other.get_props()

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.get_props()})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value is None or self.value == "":
            raise ValueError()

        if self.tag is None or self.tag == "":
            return self.value

        props = " " + self.props_to_html() if self.get_props() else ""

        if self.is_self_closing():
            return f"<{self.tag}{props} />"

        return f"<{self.tag}{props}>{self.value}</{self.tag}>"

    def __eq__(self, other: LeafNode):
        return self.tag == other.tag and self.value == other.value and self.get_props() == other.get_props()

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.get_props()})"


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
        props = " " + self.props_to_html() if self.get_props() else ""
        return f"<{self.tag}{props}>{''.join(children_list)}</{self.tag}>"
