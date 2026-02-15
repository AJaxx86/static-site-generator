import os
import shutil
from pathlib import Path

from htmlnode import HTMLNode
from md_format import extract_title, markdown_to_html_node


def static_to_public():
    if not os.path.exists("static"):
        raise Exception("Static directory does not exist")

    if os.path.exists("public"):
        print("Public already exists. Removing...")
        shutil.rmtree("public")

    shutil.copytree("static", "public")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    md_content = open(from_path, "r").read()
    template = open(template_path, "r").read()

    html_string = markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)

    html_file = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_string
    )

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(html_file)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in Path(dir_path_content).iterdir():
        if item.is_dir():
            generate_pages_recursive(Path(dir_path_content) / item.name, template_path, Path(dest_dir_path) / item.name.replace(".md", ".html"))
        else:
            generate_page(Path(dir_path_content) / item.name, template_path, Path(dest_dir_path) / item.name.replace(".md", ".html"))
    