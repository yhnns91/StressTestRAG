#!/usr/bin/env python3
"""
Compute the SHA-256 checksum of a downloaded source document.

Usage:
    python scripts/compute_checksum.py path/to/document.pdf
    python scripts/compute_checksum.py downloads/*.pdf

Paste the resulting digest into the `checksum` column of the metadata CSV.
The checksum lets anyone verify later that the file you curated is the same
file they downloaded, even if the publisher silently updates the page.
"""

import hashlib
import sys
from pathlib import Path


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.is_file():
            print(f"{arg}: not a file", file=sys.stderr)
            continue
        size_kb = path.stat().st_size / 1024
        print(f"{sha256_of(path)}  {path.name}  ({size_kb:.0f} KB)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
