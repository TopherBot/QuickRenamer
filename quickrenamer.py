#!/usr/bin/env python3
"""quickrenamer – tiny bulk file rename utility.

Usage:
    quickrenamer <glob> --pattern "new_{{index:02}}.txt" [--dry-run]

Supported tokens in the pattern:
    {{index}}      – sequential number starting at 1
    {{index:N}}    – zero‑padded to N digits (e.g. {{index:03}} → 001)
    {{name}}       – original filename without extension
    {{ext}}        – original extension (including dot)

Options:
    --dry-run      – only show what would be renamed
    -h, --help     – show this help
"""

import argparse
import glob
import os
import re
import sys
from pathlib import Path

TOKEN_REGEX = re.compile(r"\{\{\s*(index(?::(\d+))?|name|ext)\s*\}\}")

def parse_args():
    parser = argparse.ArgumentParser(description="Bulk rename files with a simple pattern.")
    parser.add_argument("files", nargs="+", help="Glob pattern(s) of files to rename")
    parser.add_argument("--pattern", "-p", required=True, help="Rename pattern, e.g. new_{{index:03}}.txt")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Show actions without performing them")
    return parser.parse_args()

def build_new_name(original: Path, pattern: str, index: int) -> str:
    def repl(match):
        token = match.group(1)
        if token.startswith("index"):
            pad = match.group(2)
            num = str(index)
            return num.zfill(int(pad)) if pad else num
        if token == "name":
            return original.stem
        if token == "ext":
            return original.suffix
        return match.group(0)  # should not happen
    return TOKEN_REGEX.sub(repl, pattern)

def main():
    args = parse_args()
    # Resolve file list
    files = []
    for pat in args.files:
        files.extend(sorted(glob.glob(pat, recursive=True)))
    if not files:
        print("No files matched the given pattern(s).", file=sys.stderr)
        sys.exit(1)

    actions = []
    for i, fp in enumerate(files, start=1):
        src = Path(fp)
        if not src.is_file():
            continue
        new_name = build_new_name(src, args.pattern, i)
        dst = src.with_name(new_name)
        # Collision handling: if dst exists, add a _dup suffix
        if dst.exists():
            stem = dst.stem
            suffix = 1
            while True:
                candidate = src.with_name(f"{stem}_dup{suffix}{dst.suffix}")
                if not candidate.exists():
                    dst = candidate
                    break
                suffix += 1
        actions.append((src, dst))

    # Show preview / execute
    for src, dst in actions:
        if args.dry_run:
            print(f"[DRY‑RUN] {src} → {dst}")
        else:
            print(f"Renaming {src} → {dst}")
            src.rename(dst)

if __name__ == "__main__":
    main()
