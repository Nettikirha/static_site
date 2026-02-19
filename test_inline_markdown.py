# test_inline_markdown.py

import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    text_to_textnodes,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
)


class TestTextToTextNodes(unittest.TestCase):
    def test_full_example(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)

    def test_plain_text(self):
        result = text_to_textnodes("Just plain text")
        self.assertEqual(result, [TextNode("Just plain text", TextType.TEXT)])

    def test_bold_only(self):
        result = text_to_textnodes("**bold**")
        self.assertEqual(result, [TextNode("bold", TextType.BOLD)])

    def test_italic_only(self):
        result = text_to_textnodes("_italic_")
        self.assertEqual(result, [TextNode("italic", TextType.ITALIC)])

    def test_code_only(self):
        result = text_to_textnodes("`code`")
        self.assertEqual(result, [TextNode("code", TextType.CODE)])

    def test_image_only(self):
        result = text_to_textnodes("![alt](https://example.com/img.png)")
        self.assertEqual(result, [TextNode("alt", TextType.IMAGE, "https://example.com/img.png")])

    def test_link_only(self):
        result = text_to_textnodes("[click](https://boot.dev)")
        self.assertEqual(result, [TextNode("click", TextType.LINK, "https://boot.dev")])

    def test_multiple_bold(self):
        result = text_to_textnodes("**one** and **two**")
        self.assertEqual(result, [
            TextNode("one", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.BOLD),
        ])

    def test_image_not_captured_as_link(self):
        result = text_to_textnodes("![img](url) and [link](url2)")
        self.assertIn(TextNode("img", TextType.IMAGE, "url"), result)
        self.assertIn(TextNode("link", TextType.LINK, "url2"), result)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold(self):
        node = TextNode("Hello **world** there", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode(" there", TextType.TEXT),
        ])

    def test_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_unmatched_delimiter_raises(self):
        node = TextNode("Hello **world", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_images(self):
        result = extract_markdown_images("![alt](url) and ![alt2](url2)")
        self.assertEqual(result, [("alt", "url"), ("alt2", "url2")])

    def test_extract_links(self):
        result = extract_markdown_links("[text](url) and [text2](url2)")
        self.assertEqual(result, [("text", "url"), ("text2", "url2")])

    def test_image_not_in_links(self):
        result = extract_markdown_links("![img](url)")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()