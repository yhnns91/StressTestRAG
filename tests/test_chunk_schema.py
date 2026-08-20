"""Tests for the Phase 2 chunk files.

These mirror the six minimum automated checks in assignment section 7.4 and the
chunk record schema in docs/schema.md, so that CI fails on a broken chunk file
rather than leaving the problem to be found by hand later.

Token counts are read from the records. Recomputing them would require tiktoken,
which downloads its encoding on first use and would make the test depend on
network access.
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CHUNK_DIR = REPO_ROOT / "corpus" / "chunks"
METADATA_DIR = REPO_ROOT / "corpus" / "metadata"
VALIDATOR = REPO_ROOT / "scripts" / "validate_chunks.py"

CHUNK_FILES = sorted(CHUNK_DIR.glob("*_chunks.jsonl"))
REQUIRED_FIELDS = {
    "chunk_id",
    "document_id",
    "heading",
    "text",
    "token_count",
    "paragraph_index",
    "source_url",
    "quality_flag",
}
OPTIONAL_FIELDS = {"note"}
QUALITY_FLAGS = {"approved", "pending", "rejected"}
CHUNK_ID = re.compile(r"^(DIS|INF|CYB)-\d{3}_C\d{2,}$")
TOKEN_MIN, TOKEN_MAX = 180, 320


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def all_chunks() -> list[dict]:
    return [record for path in CHUNK_FILES for record in load(path)]


def known_documents() -> dict[str, str]:
    known: dict[str, str] = {}
    for path in sorted(METADATA_DIR.glob("*_pilot_sources.csv")):
        with path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                doc_id = (row.get("document_id") or "").strip()
                if doc_id:
                    known[doc_id] = (row.get("source_url") or "").strip()
    return known


pytestmark = pytest.mark.skipif(not CHUNK_FILES, reason="no chunk files yet (Phase 2 not started)")


@pytest.mark.parametrize("path", CHUNK_FILES, ids=lambda p: p.name)
def test_every_line_is_valid_json(path: Path) -> None:
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if raw.strip():
            json.loads(raw)  # raises on malformed JSON, which is the failure we want


@pytest.mark.parametrize("path", CHUNK_FILES, ids=lambda p: p.name)
def test_fields_match_schema(path: Path) -> None:
    for record in load(path):
        present = set(record)
        missing = REQUIRED_FIELDS - present
        assert not missing, f"{record.get('chunk_id')}: missing {sorted(missing)}"
        unexpected = present - REQUIRED_FIELDS - OPTIONAL_FIELDS
        assert not unexpected, f"{record.get('chunk_id')}: unexpected {sorted(unexpected)}"


def test_chunk_ids_are_unique_and_well_formed() -> None:
    ids = [record["chunk_id"] for record in all_chunks()]
    duplicates = [chunk_id for chunk_id, count in Counter(ids).items() if count > 1]
    assert not duplicates, f"duplicate chunk_id: {duplicates}"
    malformed = [chunk_id for chunk_id in ids if not CHUNK_ID.match(chunk_id)]
    assert not malformed, f"malformed chunk_id: {malformed}"


def test_every_document_id_exists_in_metadata() -> None:
    known = known_documents()
    assert known, "no document ids found in corpus/metadata"
    for record in all_chunks():
        doc_id = record["document_id"]
        assert doc_id in known, f"{record['chunk_id']}: {doc_id} not in corpus/metadata"
        assert record["chunk_id"].startswith(f"{doc_id}_C")


def test_text_is_never_empty() -> None:
    empty = [r["chunk_id"] for r in all_chunks() if not str(r["text"]).strip()]
    assert not empty, f"empty text in: {empty}"


def test_token_count_in_range_or_documented() -> None:
    """Section 7.4: deviations from 180-320 need a recorded reason."""
    undocumented = [
        f"{r['chunk_id']} ({r['token_count']} tokens)"
        for r in all_chunks()
        if not TOKEN_MIN <= r["token_count"] <= TOKEN_MAX and not str(r.get("note", "")).strip()
    ]
    assert not undocumented, f"token_count outside range with no note: {undocumented}"


def test_source_trace_is_present() -> None:
    known = known_documents()
    for record in all_chunks():
        chunk_id = record["chunk_id"]
        assert str(record["heading"]).strip(), f"{chunk_id}: empty heading"
        assert record["source_url"].startswith("https://"), f"{chunk_id}: bad source_url"
        expected = known.get(record["document_id"], "")
        if expected:
            assert record["source_url"] == expected, f"{chunk_id}: source_url differs from metadata"
        assert isinstance(record["paragraph_index"], int) and record["paragraph_index"] >= 1


def test_no_exact_duplicate_text() -> None:
    seen: dict[str, str] = {}
    duplicates = []
    for record in all_chunks():
        key = re.sub(r"\s+", " ", record["text"]).strip().lower()
        if key in seen:
            duplicates.append(f"{record['chunk_id']} == {seen[key]}")
        else:
            seen[key] = record["chunk_id"]
    assert not duplicates, f"duplicate chunk text: {duplicates}"


def test_quality_flag_values_are_valid() -> None:
    for record in all_chunks():
        assert record["quality_flag"] in QUALITY_FLAGS, (
            f"{record['chunk_id']}: quality_flag {record['quality_flag']!r}"
        )


def test_flagged_chunks_record_a_reason() -> None:
    silent = [
        r["chunk_id"]
        for r in all_chunks()
        if r["quality_flag"] != "approved" and not str(r.get("note", "")).strip()
    ]
    assert not silent, f"non-approved chunks with no note: {silent}"


def test_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR)], capture_output=True, text=True, cwd=REPO_ROOT
    )
    assert result.returncode == 0, f"validate_chunks.py failed:\n{result.stdout}"
