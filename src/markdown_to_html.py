from block_markdown import *
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_leafnodes


def markdown_to_htmlnodes(markdown):
    final_htmlnode_list = []

    # markdown -> blocks and block types
    blocks = markdown_to_blocks(markdown)
    block_type_list = []
    for block in blocks:
        block_type_list.append(block_to_block_type(block))

    # pass blocks and block types to be transformed into htmlnodes
    for i in range(len(blocks)):
        if block_type_list[i] == block_type_heading:
            final_htmlnode_list.append(heading_to_htmlnode(blocks[i]))
        if block_type_list[i] == block_type_code:
            final_htmlnode_list.append(code_to_htmlnode(blocks[i]))
        if block_type_list[i] == block_type_quote:
            final_htmlnode_list.append(quote_to_htmlnode(blocks[i]))
        if block_type_list[i] == block_type_unordered_list:
            final_htmlnode_list.append(unordered_to_htmlnode(blocks[i]))
        if block_type_list[i] == block_type_ordered_list:
            final_htmlnode_list.append(ordered_to_htmlnode(blocks[i]))
        if block_type_list[i] == block_type_paragraph:
            final_htmlnode_list.extend(paragraph_to_htmlnode(blocks[i]))

    return ParentNode("div", final_htmlnode_list)


def heading_to_htmlnode(block):
    heading_count = block.count("#")
    children = text_to_leafnodes(block[heading_count + 1 :])
    return ParentNode(f"h{heading_count}", children)


def code_to_htmlnode(block):
    code_block = [LeafNode("code", block[3:-3])]
    return ParentNode("pre", code_block)


def quote_to_htmlnode(block):
    children = line_to_clean_parents(block, "p", 2)
    return ParentNode("blockquote", children)


def unordered_to_htmlnode(block):
    children = line_to_clean_parents(block, "li", 2)
    return ParentNode("ul", children)


def ordered_to_htmlnode(block):
    children = line_to_clean_parents(block, "li", None, ".")
    return ParentNode("ol", children)


def paragraph_to_htmlnode(block):
    return line_to_clean_parents(block, "p", 0)


# Takes text with newline characters and breaks it up into parentnodes
# This also cleans starting characters on each line
def line_to_clean_parents(block, parent_type, slice_start_index, leftmost_char=None):
    slice_index = slice(slice_start_index, None)
    sections = block.split("\n")
    parentnodes = []
    for section in sections:
        # only would apply to ordered lists since numbers are variable potentially
        if leftmost_char != None:
            char_index = section.index(leftmost_char)
            slice_index = slice(char_index + 2, None)
        children = text_to_leafnodes(section[slice_index])
        parentnodes.append(ParentNode(parent_type, children))
    return parentnodes
