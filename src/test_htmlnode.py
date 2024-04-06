import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        htmlnode1 = HTMLNode(
            None, None, None, {"href": "https://www.google.com", "target": "_blank"}
        )
        htmlnode2 = HTMLNode("<h1>", "This is a header", ["i", "p"], None)

        self.assertEqual(
            htmlnode1.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )
        self.assertEqual(htmlnode2.props_to_html(), "")

    def test_leafnode_to_html(self):
        leafnode1 = LeafNode("p", "This is a paragraph.")
        self.assertEqual(leafnode1.to_html(), "<p>This is a paragraph.</p>")

    def test_leafnode_to_html_with_props(self):
        leafnode2 = LeafNode("a", "Click this link", {"href": "https://www.google.com"})
        self.assertEqual(
            leafnode2.to_html(),
            '<a href="https://www.google.com">Click this link</a>',
        )

    def test_leafnode_no_tag(self):
        leafnode3 = LeafNode(None, "There is no tag here")
        self.assertEqual(leafnode3.to_html(), "There is no tag here")

    def test_parentnode_to_html(self):
        parentnode1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            parentnode1.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_parentnode_to_html_with_parentnodes(self):
        parentnode1 = ParentNode(
            "b", [ParentNode("i", [LeafNode(None, "Normal text")])]
        )

        self.assertEqual(
            parentnode1.to_html(),
            "<b><i>Normal text</i></b>",
        )

    def test_parentnode_to_html_with_parentnodes_and_leafnode(self):
        parentnode1 = ParentNode(
            "b",
            [
                ParentNode("i", [LeafNode(None, "Normal text")]),
                LeafNode("b", "Bold text"),
            ],
        )

        self.assertEqual(
            parentnode1.to_html(),
            "<b><i>Normal text</i><b>Bold text</b></b>",
        )

    def test_parentnode_to_html_with_parentnode_with_props(self):
        parentnode1 = ParentNode(
            "a",
            [ParentNode("b", [LeafNode("i", "Bold and Italic link")])],
            {"href": "https://www.google.com"},
        )

        self.assertEqual(
            parentnode1.to_html(),
            '<a href="https://www.google.com"><b><i>Bold and Italic link</i></b></a>',
        )

    def test_parentnode_to_html_with_leafnode_with_props(self):
        parentnode1 = ParentNode(
            "i",
            [
                ParentNode(
                    "b",
                    [
                        LeafNode(
                            "a",
                            "Bold and Italic link",
                            {"href": "https://www.google.com"},
                        )
                    ],
                )
            ],
        )

        self.assertEqual(
            parentnode1.to_html(),
            '<i><b><a href="https://www.google.com">Bold and Italic link</a></b></i>',
        )


if __name__ == "__main__":
    unittest.main()
