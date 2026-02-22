# src/test_markdown_to_html.py

import unittest
from markdown_to_html import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "## Hello World"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><h2>Hello World</h2></div>")

    def test_headings_all_levels(self):
        md = """# H1

## H2

### H3"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<h1>H1</h1>", html)
        self.assertIn("<h2>H2</h2>", html)
        self.assertIn("<h3>H3</h3>", html)

    def test_quote(self):
        md = "> This is a quote\n> with multiple lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertTrue(html.startswith("<div><blockquote>"))

    def test_unordered_list(self):
        md = "- Item one\n- Item two\n- Item three"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item one</li><li>Item two</li><li>Item three</li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. First\n2. Second\n3. Third"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )

    def test_inline_in_list(self):
        md = "- **bold** item\n- _italic_ item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)

    def test_multiple_block_types(self):
        md = """# Title

A paragraph with **bold**.

- item 1
- item 2"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<h1>Title</h1>", html)
        self.assertIn("<p>", html)
        self.assertIn("<ul>", html)


if __name__ == "__main__":
    unittest.main()