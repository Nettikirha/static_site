# src/test_leafnode.py

import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just raw text")
        self.assertEqual(node.to_html(), "Just raw text")

    def test_leaf_to_html_no_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_b_tag(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode("img", "", {"src": "image.jpg", "alt": "An image"})
        html = node.to_html()
        self.assertIn('src="image.jpg"', html)
        self.assertIn('alt="An image"', html)
        self.assertTrue(html.startswith("<img"))
        self.assertTrue(html.endswith("></img>"))

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello", {"class": "greeting"})
        self.assertEqual(
            repr(node),
            "LeafNode(tag=p, value=Hello, props={'class': 'greeting'})"
        )


if __name__ == "__main__":
    unittest.main()