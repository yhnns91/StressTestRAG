#!/usr/bin/env python3
"""Validate the chunk files against docs/schema.md and assignment section 7.4.

Section 7.4 lists six minimum automated checks. All six are implemented here,
plus the schema constraints that can be checked without reading the source
documents again.

The token count is read from the record rather than recomputed. Counting tokens
requires tiktoken, which downloads its encoding file on first use; the CI job
runs offline-ish and should not depend on that. build_chunks.py measures once and
stores the result.

Exit code is 0 when every file passes and 1 when any error is found, so the CI
job fails on a broken chunk file.

Usage
-----
    python scripts/validate_chunks.py
    python scripts/validate_chunks.py corpus/chunks/DIS_chunks.jsonl
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHUNK_DIR = REPO_ROOT / "corpus" / "chunks"
METADATA_DIR = REPO_ROOT / "corpus" / "metadata"

REQUIRED_FIELDS = [
    "chunk_id",
    "document_id",
    "heading",
    "text",
    "token_count",
    "paragraph_index",
    "source_url",
    "quality_flag",
]
OPTIONAL_FIELDS = ["note"]
QUALITY_FLAGS = {"approved", "pending", "rejected"}

CHUNK_ID = re.compile(r"^(DIS|INF|CYB)-\d{3}_C\d{2,}$")
TOKEN_MIN, TOKEN_MAX = 180, 320


class Report:
    def __init__(self, label: str) -> None:
        self.label = label
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"  ERROR  {where}: {message}")

    def warn(self, where: str, message: str) -> None:
        self.warnings.append(f"  WARN   {where}: {message}")

    def print(self) -> None:
        print(f"=== {self.label} ===")
        for line in self.errors:
            print(line)
        for line in self.warnings:
            print(line)
        verdict = "FAILED" if self.errors else "PASSED"
        print(f"  -> {verdict} ({len(self.errors)} error, {len(self.warnings)} warning)")


def load_known_documents() -> dict[str, str]:
    """document_id -> source_url, from the three corpus metadata files."""
    known: dict[str, str] = {}
    for path in sorted(METADATA_DIR.glob("*_pilot_sources.csv")):
        with path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                doc_id = (row.get("document_id") or "").strip()
                if doc_id:
                    known[doc_id] = (row.get("source_url") or "").strip()
    return known


def normalised_hash(text: str) -> str:
    """Hash of the text with whitespace and case flattened, for duplicate checks."""
    flat = re.sub(r"\s+", " ", text).strip().lower()
    return hashlib.sha256(flat.encode("utf-8")).hexdigest()


def validate_file(path: Path, known: dict[str, str], seen_ids: set[str]) -> Report:
    try:
        label = str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        label = str(path)          # a path given from outside the repository
    rep = Report(label)
    records: list[dict] = []

    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
        except json.JSONDecodeError as exc:
            rep.error(f"line {line_no}", f"not valid JSON ({exc.msg})")
            continue
        records.append(record)

        where = record.get("chunk_id") or f"line {line_no}"

        # -- schema: required fields present and correctly typed ---------------
        for field in REQUIRED_FIELDS:
            if field not in record:
                rep.error(where, f"missing required field {field!r}")
        for field in record:
            if field not in REQUIRED_FIELDS and field not in OPTIONAL_FIELDS:
                rep.error(where, f"unexpected field {field!r} (not in docs/schema.md)")

        # -- 7.4 check 1: chunk_id unique and correctly formed ------------------
        chunk_id = record.get("chunk_id", "")
        if not CHUNK_ID.match(str(chunk_id)):
            rep.error(where, f"chunk_id {chunk_id!r} does not match <document_id>_C<NN>")
        if chunk_id in seen_ids:
            rep.error(where, "chunk_id is not unique across the corpus")
        seen_ids.add(chunk_id)

        # -- 7.4 check 2: document_id exists in the corpus metadata -------------
        doc_id = record.get("document_id", "")
        if doc_id not in known:
            rep.error(where, f"document_id {doc_id!r} is not in corpus/metadata")
        elif not str(chunk_id).startswith(f"{doc_id}_C"):
            rep.error(where, "chunk_id prefix does not match document_id")

        # -- 7.4 check 3: text is not empty ------------------------------------
        text = record.get("text", "")
        if not str(text).strip():
            rep.error(where, "text is empty")

        # -- 7.4 check 4: token_count in range, or a reason is recorded ---------
        tokens = record.get("token_count")
        if not isinstance(tokens, int) or tokens <= 0:
            rep.error(where, f"token_count {tokens!r} is not a positive integer")
        elif not TOKEN_MIN <= tokens <= TOKEN_MAX and not str(record.get("note", "")).strip():
            rep.error(
                where,
                f"token_count {tokens} is outside {TOKEN_MIN}-{TOKEN_MAX} "
                "and no reason is recorded in note (section 7.4)",
            )

        # -- 7.4 check 5: source trace present ---------------------------------
        if not str(record.get("heading", "")).strip():
            rep.error(where, "heading is empty; source trace incomplete")
        url = str(record.get("source_url", ""))
        if not url.startswith("https://"):
            rep.error(where, "source_url missing or does not start with https://")
        elif doc_id in known and known[doc_id] and url != known[doc_id]:
            rep.error(where, "source_url does not match the value in corpus/metadata")
        index = record.get("paragraph_index")
        if not isinstance(index, int) or index < 1:
            rep.error(where, f"paragraph_index {index!r} is not a positive integer")

        # -- schema: quality_flag is one of the permitted values ---------------
        flag = record.get("quality_flag")
        if flag not in QUALITY_FLAGS:
            rep.error(where, f"quality_flag {flag!r} is not one of {sorted(QUALITY_FLAGS)}")
        elif flag != "approved" and not str(record.get("note", "")).strip():
            rep.warn(where, f"quality_flag is {flag!r} but no reason is recorded in note")

    # -- 7.4 check 6: no exact duplicates --------------------------------------
    by_hash: dict[str, list[str]] = {}
    for record in records:
        if str(record.get("text", "")).strip():
            by_hash.setdefault(normalised_hash(record["text"]), []).append(
                record.get("chunk_id", "?")
            )
    for ids in by_hash.values():
        if len(ids) > 1:
            rep.error(ids[0], f"duplicate text shared with {', '.join(ids[1:])}")

    if not records:
        rep.warn(rep.label, "file contains no chunk records")
    return rep


def main() -> int:
    known = load_known_documents()
    if not known:
        print("ERROR: no document ids found in corpus/metadata", file=sys.stderr)
        return 1

    paths = [Path(a).resolve() for a in sys.argv[1:]] or sorted(CHUNK_DIR.glob("*_chunks.jsonl"))
    if not paths:
        print(f"ERROR: no chunk files found in {CHUNK_DIR}", file=sys.stderr)
        return 1

    seen_ids: set[str] = set()
    failed = 0
    totals: Counter[str] = Counter()

    for path in paths:
        if not path.exists():
            print(f"ERROR: {path} does not exist", file=sys.stderr)
            failed += 1
            continue
        report = validate_file(path, known, seen_ids)
        report.print()
        if report.errors:
            failed += 1
        for raw in path.read_text(encoding="utf-8").splitlines():
            if raw.strip():
                try:
                    totals[json.loads(raw).get("quality_flag", "?")] += 1
                except json.JSONDecodeError:
                    pass

    print()
    print(
        f"Totals: {sum(totals.values())} chunks | "
        + " | ".join(f"{flag} {count}" for flag, count in sorted(totals.items()))
    )
    print(f"Approved chunks: {totals['approved']}   Phase 2 gate target: about 100-150")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
