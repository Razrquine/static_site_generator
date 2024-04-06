import unittest

from inline_markdown import *
from textnode import *


class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node1 = TextNode("text **bold** text", text_type_text)
        node2 = TextNode("**bold** text **bold and tough**", text_type_text)
        node_1_2_split = split_nodes_delimiter([node1, node2], "**", text_type_bold)

        self.assertEqual(node_1_2_split[1].text, "bold")
        self.assertEqual(node_1_2_split[5].text, "bold and tough")
        self.assertEqual(
            node_1_2_split,
            [
                TextNode("text ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" text", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" text ", text_type_text),
                TextNode("bold and tough", text_type_bold),
            ],
        )

        unclosed_node = TextNode("text `backtick text", text_type_text)
        with self.assertRaises(Exception) as err:
            split_nodes_delimiter([unclosed_node], "`", text_type_code)

        self.assertEqual(str(err.exception), "Closing delimiter not found")

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"

        self.assertEqual(
            extract_markdown_images(text),
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("another", "https://i.imgur.com/dfsdkjfd.png"),
            ],
        )

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"

        self.assertEqual(
            extract_markdown_links(text),
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
        )

    def test_split_nodes_image(self):
        text1 = TextNode("nothing here", text_type_text)
        text2 = TextNode("Text ![art](link) text", text_type_text)
        list_of_nodes = split_nodes_image([text1, text2])

        self.assertEqual(list_of_nodes[0].text, "nothing here")
        self.assertEqual(list_of_nodes[1].text, "Text ")
        self.assertEqual(list_of_nodes[2].text, "art")
        self.assertEqual(list_of_nodes[2].url, "link")
        self.assertEqual(list_of_nodes[3].text, " text")

    def test_split_nodes_link(self):
        text1 = TextNode("nothing here", text_type_text)
        text2 = TextNode("Text [this is link](hyperlink) text", text_type_text)
        list_of_nodes = split_nodes_link([text1, text2])

        self.assertEqual(list_of_nodes[0].text, "nothing here")
        self.assertEqual(list_of_nodes[1].text, "Text ")
        self.assertEqual(list_of_nodes[2].text, "this is link")
        self.assertEqual(list_of_nodes[2].url, "hyperlink")
        self.assertEqual(list_of_nodes[3].text, " text")

    def test_inline_markdown_to_textnodes(self):
        markdown_text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        markdown_text_textnodes = inline_markdown_to_textnodes(markdown_text)
        expected_1 = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]

        self.assertEqual(markdown_text_textnodes, expected_1)

        my_text = "text** bold **text* italic *text` code `text but woah ![image_1](image_link_1) and ![image_2](image_link_2) with [link1](link_link_1) and [link2](link_link_2)"
        expected_2 = [
            TextNode("text", text_type_text),
            TextNode(" bold ", text_type_bold),
            TextNode("text", text_type_text),
            TextNode(" italic ", text_type_italic),
            TextNode("text", text_type_text),
            TextNode(" code ", text_type_code),
            TextNode("text but woah ", text_type_text),
            TextNode("image_1", text_type_image, "image_link_1"),
            TextNode(" and ", text_type_text),
            TextNode("image_2", text_type_image, "image_link_2"),
            TextNode(" with ", text_type_text),
            TextNode("link1", text_type_link, "link_link_1"),
            TextNode(" and ", text_type_text),
            TextNode("link2", text_type_link, "link_link_2"),
        ]
        my_text_textnodes = inline_markdown_to_textnodes(my_text)

        self.assertEqual(my_text_textnodes, expected_2)
