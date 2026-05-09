import os

from src.block_helper import markdown_to_html_node, extract_title


def generate_page(basepath, from_path, template_path, dest_path):
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
    content = content.replace("href=\"/", f"href=\"{basepath}")
    content = content.replace("src=\"/", f"src=\"{basepath}")
    parent_dir = os.path.dirname(dest_path)
    if parent_dir != "":
        os.makedirs(parent_dir, 0o755, exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(content)


def collect_paths(root_path, known_paths):
    paths = os.listdir(root_path)
    for path in paths:
        path = os.path.join(root_path, path)
        if os.path.isdir(path):
            collect_paths(path, known_paths)
        elif os.path.isfile(path):
            known_paths.append(path)
    return known_paths


def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    file_paths = collect_paths(dir_path_content, [])
    for file in file_paths:
        file_dest_path = file.replace(dir_path_content, dest_dir_path).replace("md", "html")
        generate_page(basepath, file, template_path, file_dest_path)
