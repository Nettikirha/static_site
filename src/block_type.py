# src/block_type.py

from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    # Heading: 1-6 # characters followed by a space
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING

    # Code block: starts with ``` and newline, ends with ```
    if block.startswith('```\n') and block.endswith('```'):
        return BlockType.CODE

    lines = block.split('\n')

    # Quote: every line starts with >
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with "- "
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: lines start with 1. 2. 3. etc.
    is_ordered = True
    for i, line in enumerate(lines):
        if not line.startswith(f'{i + 1}. '):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH