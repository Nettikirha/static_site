# test_inline_markdown.py

import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_image, split_nodes_link


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode("![only image](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("only image", TextType.IMAGE, "https://example.com/img.png")],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode("![image](https://example.com/img.png) followed by text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_end(self):
        node = TextNode("text before ![image](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("text before ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            ],
            new_nodes,
        )

    def test_split_image_no_images(self):
        node = TextNode("This is plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_image_non_text_node_passed_through(self):
        node = TextNode("bold text", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_image_multiple_nodes(self):
        node1 = TextNode("Text ![img1](https://example.com/1.png) middle", TextType.TEXT)
        node2 = TextNode("already bold", TextType.BOLD)
        node3 = TextNode("more text ![img2](https://example.com/2.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "https://example.com/1.png"),
                TextNode(" middle", TextType.TEXT),
                TextNode("already bold", TextType.BOLD),
                TextNode("more text ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "https://example.com/2.png"),
            ],
            new_nodes,
        )

    def test_split_image_does_not_match_links(self):
        # A plain link should not be extracted as an image
        node = TextNode("A [link](https://example.com) here", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_image_empty_alt_text(self):
        node = TextNode("before ![](https://example.com/img.png) after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_link_single(self):
        node = TextNode("[only link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("only link", TextType.LINK, "https://example.com")],
            new_nodes,
        )

    def test_split_link_at_start(self):
        node = TextNode("[link](https://example.com) followed by text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode("text before [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("text before ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_link_no_links(self):
        node = TextNode("This is plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_link_non_text_node_passed_through(self):
        node = TextNode("italic text", TextType.ITALIC)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_link_does_not_match_images(self):
        # An image should not be extracted as a link
        node = TextNode("An ![image](https://example.com/img.png) here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_link_multiple_nodes(self):
        node1 = TextNode("Text [link1](https://a.com) middle", TextType.TEXT)
        node2 = TextNode("bold text", TextType.BOLD)
        node3 = TextNode("more [link2](https://b.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://a.com"),
                TextNode(" middle", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode("more ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://b.com"),
            ],
            new_nodes,
        )

    def test_split_link_empty_input(self):
        new_nodes = split_nodes_link([])
        self.assertListEqual([], new_nodes)

    def test_split_image_empty_input(self):
        new_nodes = split_nodes_image([])
        self.assertListEqual([], new_nodes)


if __name__ == "__main__":
    unittest.main()