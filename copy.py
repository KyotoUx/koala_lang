#!/usr/bin/env python3.9

from argparse import ArgumentParser
from pathlib import Path
from shutil import copy
import sys

PATTERN = "edx-platform.*"
HERE = Path(__file__).parent.resolve()

DESCRIPTION ='This script copies ".po" file under specific directory. use like: `./copy.py . ./dist && cp -r ./dist/* "$(tutor config printroot)/env/build/openedx/locale/ja-jp/LC_MESSAGES"'


def parse_args() -> tuple[Path, Path]:
    parser = ArgumentParser(epilog=DESCRIPTION)
    parser.add_argument(
        "--src",
        type=Path,
        default=HERE,
        help="Path to source directory, default is . (repository root)",
    )
    parser.add_argument(
        "--dist",
        type=Path,
        default=HERE / "dist",
        help="Path to distribution directory, default is ./dist",
    )

    args = parser.parse_args()
    return args.src, args.dist


def copy_files(src: Path, dist: Path):
    for p in src.glob(PATTERN):
        po_file = p / "ja_JP.po"
        filename = po_file.parent.name.removeprefix(PATTERN.removesuffix("*")) + ".po"
        if po_file.exists():
            dest = dist / filename
            copy(po_file, dest)
            print(f"COPY: {po_file} -> {dest}")


def main():
    src, dist = parse_args()
    if not dist.exists():
        print(f"{dist} dose not exists, making")
        dist.mkdir()

    copy_files(src, dist)


if __name__ == "__main__":
    main()
