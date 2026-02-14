# src/test_parentnode.py

import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>',
        )

    def test_to_html_no_tag_raises_error(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("tag", str(context.exception).lower())

    def test_to_html_no_children_raises_error(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("children", str(context.exception).lower())

    def test_to_html_empty_children_list(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_nested_parent_nodes(self):
        # Deep nesting: div > p > span > b
        innermost = LeafNode("b", "bold text")
        span_node = ParentNode("span", [innermost])
        p_node = ParentNode("p", [span_node])
        div_node = ParentNode("div", [p_node])
        self.assertEqual(
            div_node.to_html(),
            "<div><p><span><b>bold text</b></span></p></div>",
        )

    def test_to_html_mixed_parent_and_leaf_children(self):
        # Parent with both leaf and parent children
        leaf1 = LeafNode("b", "Bold")
        parent_child = ParentNode("span", [LeafNode("i", "Italic")])
        leaf2 = LeafNode(None, "Normal")
        parent_node = ParentNode("p", [leaf1, parent_child, leaf2])
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold</b><span><i>Italic</i></span>Normal</p>",
        )

    def test_to_html_complex_nested_structure(self):
        # ul > li > a structure
        link1 = LeafNode("a", "Link 1", {"href": "/page1"})
        link2 = LeafNode("a", "Link 2", {"href": "/page2"})
        li1 = ParentNode("li", [link1])
        li2 = ParentNode("li", [link2])
        ul = ParentNode("ul", [li1, li2])
        self.assertEqual(
            ul.to_html(),
            '<ul><li><a href="/page1">Link 1</a></li><li><a href="/page2">Link 2</a></li></ul>',
        )

    def test_to_html_many_siblings(self):
        children = [LeafNode("span", f"child{i}") for i in range(5)]
        parent_node = ParentNode("div", children)
        expected = "<div>" + "".join(f"<span>child{i}</span>" for i in range(5)) + "</div>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_repr(self):
        child = LeafNode("span", "text")
        parent = ParentNode("div", [child], {"class": "wrapper"})
        repr_str = repr(parent)
        self.assertIn("ParentNode", repr_str)
        self.assertIn("tag=div", repr_str)
        self.assertIn("children=", repr_str)
        self.assertIn("props=", repr_str)


if __name__ == "__main__":
    unittest.main()
