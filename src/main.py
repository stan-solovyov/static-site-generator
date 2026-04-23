from pathlib import Path
import sys

from helpers.helper_functions import generate_page, generate_pages_recursive


def delete_path(path):
    if not path.exists():
        return
    if path.is_dir():
        for child in path.iterdir():
            delete_path(child)
        path.rmdir()
        return
    path.unlink()


def copy_path(source, destination):
    if source.is_dir():
        destination.mkdir(exist_ok=True)
        for child in source.iterdir():
            copy_path(child, destination / child.name)
        return
    destination.write_bytes(source.read_bytes())


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    project_root = Path(__file__).resolve().parent.parent
    static_dir = project_root / "static"
    public_dir = project_root / "docs"

    delete_path(public_dir)
    copy_path(static_dir, public_dir)
    generate_pages_recursive(project_root / "content", project_root / "template.html", public_dir, basepath)


if __name__ == "__main__":
    main()
