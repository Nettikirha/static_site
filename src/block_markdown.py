# src/block_markdown.py

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        block = block.strip()
        if block:
            result.append(block)
    return result


def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "heading"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return "quote"
    if all(line.startswith("- ") for line in lines):
        return "unordered_list"
    if all(line.startswith("* ") for line in lines):
        return "unordered_list"
    is_ordered = True
    for i, line in enumerate(lines):
        if not line.startswith(f"{i+1}. "):
            is_ordered = False
            break
    if is_ordered:
        return "ordered_list"
    return "paragraph"