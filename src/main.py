# src/main.py

import os
import sys
import shutil

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def copy_static(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copyfile(src_path, dst_path)
        else:
            print(f"Entering directory: {src_path}")
            copy_static(src_path, dst_path)


def main():
    from generate_page import generate_pages_recursive

    # Get basepath from CLI argument, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    static_dir = os.path.join(PROJECT_ROOT, "static")
    docs_dir = os.path.join(PROJECT_ROOT, "docs")
    copy_static(static_dir, docs_dir)

    generate_pages_recursive(
        os.path.join(PROJECT_ROOT, "content"),
        os.path.join(PROJECT_ROOT, "template.html"),
        docs_dir,
        basepath,
    )


if __name__ == "__main__":
    main()