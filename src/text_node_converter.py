# src/text_node_converter.py

from textnode import TextNode, TextType
from leafnode import LeafNode


def text_node_to_html_node(text_node):
    """
    Convert a TextNode to an HTMLNode (specifically a LeafNode).
    
    Args:
        text_node: A TextNode object to convert
        
    Returns:
        A LeafNode object representing the HTML equivalent
        
    Raises:
        ValueError: If the text_node has an unsupported TextType
    """
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    
    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")
