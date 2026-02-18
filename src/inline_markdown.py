# src/inline_markdown.py

import re
from textnode import TextNode, TextType


def extract_markdown_images(text):
    """Extract all markdown images as (alt, url) tuples."""
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    """Extract all markdown links as (anchor, url) tuples."""
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    """
    Split TextNodes on markdown image syntax into TEXT and IMAGE nodes.
    
    Args:
        old_nodes: List of TextNode objects
        
    Returns:
        List of TextNode objects with image markdown replaced by IMAGE nodes
    """
    new_nodes = []
    for node in old_nodes:
        # Only process TEXT type nodes; pass others through unchanged
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for alt, url in images:
            sections = remaining_text.split(f"![{alt}]({url})", 1)
            if sections[0]:  # Don't add empty text nodes
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining_text = sections[1]

        if remaining_text:  # Don't add empty text nodes
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    """
    Split TextNodes on markdown link syntax into TEXT and LINK nodes.
    
    Args:
        old_nodes: List of TextNode objects
        
    Returns:
        List of TextNode objects with link markdown replaced by LINK nodes
    """
    new_nodes = []
    for node in old_nodes:
        # Only process TEXT type nodes; pass others through unchanged
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for anchor, url in links:
            sections = remaining_text.split(f"[{anchor}]({url})", 1)
            if sections[0]:  # Don't add empty text nodes
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            remaining_text = sections[1]

        if remaining_text:  # Don't add empty text nodes
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes