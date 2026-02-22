# src/markdown_to_html.py

from block_markdown import markdown_to_blocks, block_to_block_type
from inline_markdown import text_to_textnodes
from text_node_converter import text_node_to_html_node
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in text_nodes]


def heading_block_to_node(block):
    level = 0
    for ch in block:
        if ch == "#":
            level += 1
        else:
            break
    text = block[level + 1:]  # skip "# "
    return ParentNode(f"h{level}", text_to_children(text))


def code_block_to_node(block):
    # Strip the ``` fences
    content = block[3:-3]
    if content.startswith("\n"):
        content = content[1:]
    code_node = text_node_to_html_node(TextNode(content, TextType.CODE))
    return ParentNode("pre", [code_node])


def quote_block_to_node(block):
    lines = block.split("\n")
    stripped = "\n".join(line.lstrip(">").lstrip(" ") for line in lines)
    return ParentNode("blockquote", text_to_children(stripped))


def unordered_list_block_to_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        text = line[2:]  # strip "- " or "* "
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", items)


def ordered_list_block_to_node(block):
    lines = block.split("\n")
    items = []
    for i, line in enumerate(lines):
        text = line[len(f"{i+1}. "):]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)


def paragraph_block_to_node(block):
    # Join lines with spaces
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            children.append(heading_block_to_node(block))
        elif block_type == "code":
            children.append(code_block_to_node(block))
        elif block_type == "quote":
            children.append(quote_block_to_node(block))
        elif block_type == "unordered_list":
            children.append(unordered_list_block_to_node(block))
        elif block_type == "ordered_list":
            children.append(ordered_list_block_to_node(block))
        else:
            children.append(paragraph_block_to_node(block))
    return ParentNode("div", children)