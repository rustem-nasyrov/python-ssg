import sys

from src.generator import generate_pages_recursive
from src.static_to_public import copy_static_to_public


def main() -> None:
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static_to_public()
    generate_pages_recursive(basepath, "content", "template.html", "docs")


if __name__ == "__main__":
    main()
