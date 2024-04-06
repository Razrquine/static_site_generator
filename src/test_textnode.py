import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        node3 = TextNode("This is a text node", "italics")
        node4 = TextNode("This is a text node", "italics")
        node5 = TextNode("This is a text node", "bold", "https://www.kekw.lol")
        node6 = TextNode("This is a text node", "bold", "https://www.kekw.lol")
        self.assertEqual(node1, node2)  # expect true
        self.assertEqual(node3, node4)  # expect true
        self.assertEqual(node5, node6)  # expect true

    def test_textnode_to_htmlnode_all_types(self):
        node_text = textnode_to_htmlnode(TextNode("Text node", "text"))
        node_bold = textnode_to_htmlnode(TextNode("Bold node", "bold"))
        node_italic = textnode_to_htmlnode(TextNode("Italic node", "italic"))
        node_code = textnode_to_htmlnode(TextNode("Code node", "code"))
        node_link = textnode_to_htmlnode(
            TextNode("Link node", "link", "https://www.wtf.com")
        )
        node_image = textnode_to_htmlnode(
            TextNode("Image node", "image", "https://www.wtf.com/images/lmao.jpg")
        )

        self.assertEqual(node_text.to_html(), "Text node")
        self.assertEqual(node_bold.to_html(), "<b>Bold node</b>")
        self.assertEqual(node_italic.to_html(), "<i>Italic node</i>")
        self.assertEqual(node_code.to_html(), "<code>Code node</code>")
        self.assertEqual(
            node_link.to_html(), '<a href="https://www.wtf.com">Link node</a>'
        )
        self.assertEqual(
            node_image.to_html(),
            '<img src="https://www.wtf.com/images/lmao.jpg" alt="Image node"></img>',
        )
        with self.assertRaises(Exception) as err:
            textnode_to_htmlnode(TextNode("Wtf is this", "nope"))

        self.assertEqual(str(err.exception), "TextNode text_type invalid: nope")


if __name__ == "__main__":
    unittest.main()
