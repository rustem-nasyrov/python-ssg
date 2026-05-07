import os
import shutil


def copy_static_to_public(static_dir: str = "static", public_dir: str = "public") -> None:
    static_path = os.path.abspath(static_dir)
    public_path = os.path.abspath(public_dir)

    if not os.path.exists(static_path):
        raise FileNotFoundError(f"Source directory not found: {static_path}")

    if os.path.exists(public_path):
        print(f"Removing destination directory: {public_path}")
        shutil.rmtree(public_path)

    os.makedirs(public_path, exist_ok=True)

    def _copy_dir(src: str, dst: str) -> None:
        for name in os.listdir(src):
            src_item = os.path.join(src, name)
            dst_item = os.path.join(dst, name)
            if os.path.isfile(src_item):
                os.makedirs(os.path.dirname(dst_item), exist_ok=True)
                shutil.copy2(src_item, dst_item)
                print(f"Copied: {src_item} -> {dst_item}")
            elif os.path.isdir(src_item):
                os.makedirs(dst_item, exist_ok=True)
                _copy_dir(src_item, dst_item)

    _copy_dir(static_path, public_path)
