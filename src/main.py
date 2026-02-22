# src/main.py

import os
import shutil
from textnode import TextNode, TextType

# Resolve paths relative to this file (src/main.py), go up one level to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def copy_static(src, dst):
    # On the initial call, clear the destination directory
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
    static_dir = os.path.join(PROJECT_ROOT, "static")
    public_dir = os.path.join(PROJECT_ROOT, "public")
    copy_static(static_dir, public_dir)


if __name__ == "__main__":
    main()