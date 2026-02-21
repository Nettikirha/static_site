import unittest
from block_type import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    # Heading tests
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)

    def test_heading_h3(self):
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_heading_too_many_hashes(self):
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)

    def test_heading_no_space(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    # Code block tests
    def test_code_block(self):
        block = "```\nsome code here\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_multiline(self):
        block = "```\ndef foo():\n    return 42\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_missing_end(self):
        block = "```\nsome code here"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_missing_newline_after_start(self):
        block = "```some code```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Quote tests
    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type(">This is a quote"), BlockType.QUOTE)

    def test_quote_with_space(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)

    def test_quote_multiline(self):
        block = ">Line one\n>Line two\n>Line three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_not_all_lines(self):
        block = ">Line one\nLine two without >"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Unordered list tests
    def test_unordered_list_single(self):
        self.assertEqual(block_to_block_type("- Item one"), BlockType.UNORDERED_LIST)

    def test_unordered_list_multiple(self):
        block = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space(self):
        self.assertEqual(block_to_block_type("-Item"), BlockType.PARAGRAPH)

    def test_unordered_list_not_all_lines(self):
        block = "- Item one\nItem two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Ordered list tests
    def test_ordered_list_single(self):
        self.assertEqual(block_to_block_type("1. First item"), BlockType.ORDERED_LIST)

    def test_ordered_list_multiple(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start(self):
        block = "2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_wrong_increment(self):
        block = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_missing_space(self):
        self.assertEqual(block_to_block_type("1.No space"), BlockType.PARAGRAPH)

    # Paragraph tests
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just some plain text."), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        block = "First line\nSecond line\nThird line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()