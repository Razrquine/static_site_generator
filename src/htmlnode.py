class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # string with html tag name
        self.value = value  # string with html content
        self.children = children  # list of html node objects
        self.props = props  # dictionary of html tag attributes

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        result = ""
        if self.props == None:
            return result
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("There is no value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


# children needs to be LeafNodes
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("There is no tag")
        if self.children == None:
            raise ValueError("There are no children")
        result = ""
        for node in self.children:
            result += node.to_html()

        return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
