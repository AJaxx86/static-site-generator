import os
import sys

from file_funcs import generate_pages_recursive, static_to_public

base_path = sys.argv[1] if len(sys.argv) > 1 else "/"

static_to_public()

generate_pages_recursive(
    base_path, "content", "template.html", "docs"
)
