from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, props)
        self.children = children or []

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to convert to HTML")
        if not self.children:
            raise ValueError("ParentNode must have children to convert to HTML")
        return f"<{self.tag}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"