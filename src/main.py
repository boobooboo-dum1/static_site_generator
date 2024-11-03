import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
PUBLIC_DIR = BASE_DIR / "public"


def copy_fs_tree(source: Path, destination: Path):
    if destination.exists and destination.is_dir:
        shutil.rmtree(destination)

    shutil.copytree(source, destination)


def main():
    copy_fs_tree(STATIC_DIR, PUBLIC_DIR)


if __name__ == "__main__":
    main()
