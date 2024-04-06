import os
import shutil

from block_markdown import markdown_to_blocks
from markdown_to_html import markdown_to_htmlnodes


def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    # delete everything in the destination directory
    if os.path.exists(dest_dir_path):
        print(f"removed {dest_dir_path}")
        shutil.rmtree(dest_dir_path)

    # create directory at destination so that the base case check can happen
    os.mkdir(dest_dir_path)
    print("made destination")

    # base case: if the source and destination subdirectories are the same, break out
    # if os.listdir(dest_dir_path) == os.listdir(dir_path_content):
    #     print("base case reached")
    #     return

    for subdirectory in os.listdir(dir_path_content):
        new_dir_path_content = os.path.join(dir_path_content, subdirectory)
        new_dest_dir_path = os.path.join(dest_dir_path, subdirectory)
        print(f"{new_dir_path_content} -> {new_dest_dir_path}")

        if os.path.isfile(new_dir_path_content):
            generate_page(
                new_dir_path_content, template_path, new_dest_dir_path[:-2] + "html"
            )
        else:
            generate_pages_recursively(
                new_dir_path_content, template_path, new_dest_dir_path
            )


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, encoding="utf-8") as f:
        markdown = f.read()
    with open(template_path, encoding="utf-8") as f:
        template = f.read()
    content = markdown_to_htmlnodes(markdown).to_html()
    title = extract_title(markdown)

    html = template.replace("{{ Title }}", title)
    final_html = html.replace("{{ Content }}", content)

    # if not os.path.exists(os.path.dirname(dest_path)):
    #     os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    if blocks[0].startswith("# "):
        return blocks[0][2:]
    else:
        raise Exception("No top level header(title) available")
