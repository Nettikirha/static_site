# src/test_markdown_extracts.py

import unittest
from markdown_extracts import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_single_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_no_images(self):
        text = "This is plain text with no images."
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_image_ignores_plain_links(self):
        text = "Here is a [link](https://example.com) but no image."
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_image_empty_alt_text(self):
        text = "An image with no alt: ![](https://example.com/img.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://example.com/img.png")], matches)

    def test_extract_image_mixed_content(self):
        text = "Start ![first](https://a.com/1.png) middle [a link](https://b.com) end ![second](https://c.com/2.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("first", "https://a.com/1.png"), ("second", "https://c.com/2.jpg")],
            matches,
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_single_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_no_links(self):
        text = "This is plain text with no links."
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_links_ignores_images(self):
        text = "Here is an image ![alt text](https://example.com/img.png) but no link."
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_link_empty_anchor_text(self):
        text = "A link with no anchor: [](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://example.com")], matches)

    def test_extract_links_mixed_with_images(self):
        text = "A ![photo](https://img.com/a.png) and a [link](https://site.com) together."
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://site.com")], matches)


if __name__ == "__main__":
    unittest.main()