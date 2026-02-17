# src/markdown_extracts.py

import re


def extract_markdown_images(text):
    """
    Extracts all markdown images from a string.
    Returns a list of (alt_text, url) tuples.
    """
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    """
    Extracts all markdown links (not images) from a string.
    Returns a list of (anchor_text, url) tuples.
    """
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)