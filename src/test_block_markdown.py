import unittest

from block_markdown import *
from textnode import *


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = "wtf    \n\n   This a new block?  \n\n\n\n\n > Noway\nVery next one"
        expected = ["wtf", "This a new block?", "> Noway\nVery next one"]
        blocked = markdown_to_blocks(markdown)

        self.assertEqual(blocked, expected)

    def test_block_to_block_type(self):
        paragraph = "Just some text"
        heading = "### Heading"
        code = "```\ncode here\n```"
        quote = "> This is\n> a great\n> quote"
        unordered = "* first\n* second\n- third"
        ordered = "1. one\n2. two\n3. three"

        self.assertEqual(block_to_block_type(paragraph), block_type_paragraph)
        self.assertEqual(block_to_block_type(heading), block_type_heading)
        self.assertEqual(block_to_block_type(code), block_type_code)
        self.assertEqual(block_to_block_type(quote), block_type_quote)
        self.assertEqual(block_to_block_type(unordered), block_type_unordered_list)
        self.assertEqual(block_to_block_type(ordered), block_type_ordered_list)

        not_heading = "###Heading"
        not_code = "```\ncode blah blah here\n``"
        not_quote = "> This is\n>> a great\n> quote"
        not_unordered = "* first\n& second\n- third"
        not_ordered = "3. one\n2. two\n1. three"

        self.assertEqual(block_to_block_type(not_heading), block_type_paragraph)
        self.assertEqual(block_to_block_type(not_code), block_type_paragraph)
        self.assertEqual(block_to_block_type(not_quote), block_type_paragraph)
        self.assertEqual(block_to_block_type(not_unordered), block_type_paragraph)
        self.assertEqual(block_to_block_type(not_ordered), block_type_paragraph)
