import shutil
from pathlib import Path

from generate import generate_page

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
PUBLIC_DIR = BASE_DIR / "public"
TEMPLATE_PATH = BASE_DIR / "template.html"

CONTENT_PATH = BASE_DIR / "content/index.md"
DEST_PATH = BASE_DIR / "public/index.html"


def copy_fs_tree(source: Path, destination: Path):
    if destination.exists and destination.is_dir:
        shutil.rmtree(destination)

    shutil.copytree(source, destination)


def main():
    content_path = BASE_DIR / "content/index.md"
    dest_path = BASE_DIR / "public/index.html"

    copy_fs_tree(STATIC_DIR, PUBLIC_DIR)
    generate_page(content_path, TEMPLATE_PATH, dest_path)


if __name__ == "__main__":
    main()
