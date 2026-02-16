# src/split_delimiter.py

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split text nodes based on a delimiter and create new nodes with the specified text type.
    
    Args:
        old_nodes: List of TextNode objects to process
        delimiter: String delimiter to split on (e.g., "**", "*", "`")
        text_type: TextType to assign to the delimited text
        
    Returns:
        List of TextNode objects with delimited sections converted to the specified type
        
    Raises:
        ValueError: If a closing delimiter is not found (invalid Markdown syntax)
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process TEXT type nodes; others pass through unchanged
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Split the text by the delimiter
        sections = old_node.text.split(delimiter)
        
        # If there's an odd number of sections, we have unmatched delimiters
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: unmatched delimiter '{delimiter}'")
        
        # Process each section
        for i, section in enumerate(sections):
            # Skip empty sections
            if section == "":
                continue
            
            # Even indices (0, 2, 4...) are normal text
            # Odd indices (1, 3, 5...) are delimited text
            if i % 2 == 0:
                new_nodes.append(TextNode(section, TextType.TEXT))
            else:
                new_nodes.append(TextNode(section, text_type))
    
    return new_nodes