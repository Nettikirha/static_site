# src/test_extract_title.py

import unittest
from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello World  "), "Hello World")

    def test_title_in_multiline(self):
        md = "Some text\n# My Title\nMore text"
        self.assertEqual(extract_title(md), "My Title")

    def test_ignores_h2(self):
        md = "## Not a title\n# Real Title"
        self.assertEqual(extract_title(md), "Real Title")

    def test_no_h1_raises(self):
        with self.assertRaises(ValueError):
            extract_title("## Only h2\nNo h1 here")

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            extract_title("")

    def test_first_h1_returned(self):
        md = "# First\n# Second"
        self.assertEqual(extract_title(md), "First")


if __name__ == "__main__":
    unittest.main()