from src.generator import generate_pages_recursive
from src.static_to_public import copy_static_to_public


def main() -> None:
    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
