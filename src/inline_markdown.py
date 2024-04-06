import re

from textnode import *


# Takes text and converts it to a list of children
def text_to_leafnodes(text):
    children_textnode_list = inline_markdown_to_textnodes(text)
    children_leafnode_list = []
    for node in children_textnode_list:
        children_leafnode_list.append(textnode_to_htmlnode(node))
    return children_leafnode_list


# Takes a line of text and converts it to a list of TextNodes
def inline_markdown_to_textnodes(text):
    new_nodes = [TextNode(text, text_type_text)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", text_type_bold)
    new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
    new_nodes = split_nodes_delimiter(new_nodes, "`", text_type_code)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # act only on nodes of type text or ones with links in them
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        split_nodes = node.text.split(delimiter)
        # check is delimiter is closed
        if len(split_nodes) % 2 == 0:
            raise Exception("Closing delimiter not found")
        for i in range(len(split_nodes)):
            if split_nodes[i] == "":
                continue
            # split results in "" if it was split at start of string
            # This means even indexed items in the list are always text type
            if i % 2 == 0:
                new_nodes.append(TextNode(split_nodes[i], text_type_text))
            else:
                new_nodes.append(TextNode(split_nodes[i], text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # act only on nodes of type text or ones with links in them
        if "](" not in node.text or node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        # split text and append text and image nodes
        delimiter = extract_markdown_images(node.text)
        processing_text = node.text
        for image in delimiter:
            split_list = processing_text.split(f"![{image[0]}]({image[1]})", 1)
            if split_list[0] != "":
                new_nodes.append(TextNode(split_list[0], text_type_text))

            new_nodes.append(TextNode(image[0], text_type_image, image[1]))
            processing_text = split_list[1]

        # after the loop is done processing images, append leftover text
        if processing_text != "":
            new_nodes.append(TextNode(processing_text, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # act only on nodes of type text
        if "](" not in node.text or node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        # split text and append text and link nodes
        delimiter = extract_markdown_links(node.text)
        processing_text = node.text
        for link in delimiter:
            split_list = processing_text.split(f"[{link[0]}]({link[1]})", 1)
            if split_list[0] != "":
                new_nodes.append(TextNode(split_list[0], text_type_text))

            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            processing_text = split_list[1]
        ############### somewhere here needs to be an "endswith(".md")"
        ############### so I can change links into html links

        # after the loop is done processing links, append leftover text
        if processing_text != "":
            new_nodes.append(TextNode(processing_text, text_type_text))
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)
