import unittest

from markdown_to_html import *


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_htmlnodes(self):
        markdown = "# Title\n\n> *That's crazy*\n> -By **wise man**\n\n```WHERE IS THE EXE```\n\n- huh that's *italic*\n* what\n\n1. But\n2. No\n\nRegular text `then code!` and text\nNext line for this paragraph"
        expected = "<div><h1>Title</h1><blockquote><p><i>That's crazy</i></p><p>-By <b>wise man</b></p></blockquote><pre><code>WHERE IS THE EXE</code></pre><ul><li>huh that's <i>italic</i></li><li>what</li></ul><ol><li>But</li><li>No</li></ol><p>Regular text <code>then code!</code> and text</p><p>Next line for this paragraph</p></div>"

        htmlnodes = markdown_to_htmlnodes(markdown)
        html = htmlnodes.to_html()
        self.assertEqual(html, expected)
