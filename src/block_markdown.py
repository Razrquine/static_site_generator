block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = []
    split = markdown.split("\n\n")
    for item in split:
        if item == "":
            continue
        blocks.append(item.lstrip("\n").strip(" "))
    return blocks


def block_to_block_type(markdown):
    sections = markdown.split("\n")
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    if markdown.startswith("```") and markdown.endswith("```"):
        return block_type_code
    if all(section.startswith("> ") for section in sections):
        return block_type_quote
    if all(section.startswith(("* ", "- ")) for section in sections):
        return block_type_unordered_list
    if all(sections[i].startswith(f"{i+1}. ") for i in range(len(sections))):
        return block_type_ordered_list
    return block_type_paragraph
