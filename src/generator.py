import os

from src.block_helper import markdown_to_html_node, extract_title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = None
    with open(os.path.normpath(from_path)) as opened_file:
        markdown = opened_file.read()
    template = None
    with open(os.path.normpath(template_path)) as opened_file:
        template = opened_file.read()
    markdown_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    content = template.replace("{{ Content }}", markdown_html)
    parent_dir = os.path.dirname(dest_path)
    if parent_dir != "":
        os.makedirs(parent_dir, 0o755, exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(content)
