import os

from file_funcs import generate_pages_recursive, static_to_public

static_to_public()

generate_pages_recursive("content", "template.html", "public")
