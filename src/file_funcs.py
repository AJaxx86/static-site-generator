import os
import shutil


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
