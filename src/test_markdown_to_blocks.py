import unittest
from markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])

    def test_single_block(self):
        blocks = markdown_to_blocks("Just one paragraph")
        self.assertEqual(blocks, ["Just one paragraph"])

    def test_excessive_newlines(self):
        md = "Block one\n\n\n\nBlock two"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block one", "Block two"])

    def test_strips_whitespace(self):
        md = "   Block one   \n\n   Block two   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block one", "Block two"])

    def test_heading_paragraph_list(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
        ])


if __name__ == "__main__":
    unittest.main()