# src/test_split_delimiter.py

import unittest
from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_code_delimiter(self):
        """Test splitting with code backticks"""
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_bold_delimiter(self):
        """Test splitting with bold delimiters"""
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_italic_delimiter(self):
        """Test splitting with italic delimiters"""
        node = TextNode("An *italic word* here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("An ", TextType.TEXT),
            TextNode("italic word", TextType.ITALIC),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_multiple_delimiters(self):
        """Test with multiple occurrences of the delimiter"""
        node = TextNode("Code `here` and `there` too", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Code ", TextType.TEXT),
            TextNode("here", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("there", TextType.CODE),
            TextNode(" too", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_delimiter_at_start(self):
        """Test when delimiter starts at the beginning"""
        node = TextNode("**bold** at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_delimiter_at_end(self):
        """Test when delimiter is at the end"""
        node = TextNode("End with **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("End with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_entire_string_delimited(self):
        """Test when the entire string is delimited"""
        node = TextNode("`all code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("all code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_no_delimiter(self):
        """Test when there's no delimiter in the text"""
        node = TextNode("No formatting here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("No formatting here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_non_text_node_passes_through(self):
        """Test that non-TEXT nodes are not modified"""
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Already bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_multiple_nodes_input(self):
        """Test with multiple nodes in the input list"""
        nodes = [
            TextNode("First `code` here", TextType.TEXT),
            TextNode("Already italic", TextType.ITALIC),
            TextNode("Second `code` there", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
            TextNode("Already italic", TextType.ITALIC),
            TextNode("Second ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" there", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_unmatched_delimiter_raises_error(self):
        """Test that unmatched delimiters raise an error"""
        node = TextNode("This has `unmatched delimiter", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("Invalid Markdown syntax", str(context.exception))
        self.assertIn("unmatched delimiter", str(context.exception))
    
    def test_three_delimiters_raises_error(self):
        """Test that three delimiters (odd number) raises an error"""
        node = TextNode("One `two` three `four", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("Invalid Markdown syntax", str(context.exception))
    
    def test_empty_delimited_section(self):
        """Test with empty content between delimiters"""
        node = TextNode("Empty `` delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        # Empty sections should be skipped
        expected = [
            TextNode("Empty ", TextType.TEXT),
            TextNode(" delimiters", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_consecutive_delimiters(self):
        """Test with consecutive different delimited sections"""
        node = TextNode("`code1``code2`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code1", TextType.CODE),
            TextNode("code2", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()