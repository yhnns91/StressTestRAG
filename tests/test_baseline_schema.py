"""Tests for the Phase 3 baseline questions file.

These mirror docs/schema.md section 3 and the writing rules in assignment
section 8.4, so that CI fails on a broken baseline file rather than leaving the
problem to be found during annotation in Phase 5.

The file is skipped when it does not exist yet, so the suite stays green before
Phase 3 begins.
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
BASELINE_PATH = REPO_ROOT / "data" / "interim" / "baseline_questions.csv"
METADATA_DIR = REPO_ROOT / "corpus" / "metadata"
CHUNK_DIR = REPO_ROOT / "corpus" / "chunks"
VALIDATOR = REPO_ROOT / "scripts" / "validate_baselines.py"

REQUIRED_COLUMNS = [
    "scenario_id",
    "domain",
    "document_id",
    "expected_retrieval_chunk_ids",
    "baseline_question",
    "ground_truth_context",
    "ground_truth_answer",
    "question_type",
    "answerability_label",
    "reviewer_status",
]
DOMAINS = {
    "DIS": "natural_disaster",
    "INF": "infrastructure_disruption",
    "CYB": "cyber_incident_response",
}
QUESTION_TYPES = {
    "factual_information",
    "procedural_guidance",
    "clarification",
    "resource_seeking",
    "prioritization",
    "misinformation_correction",
}
SCENARIO_ID = re.compile(r"^(DIS|INF|CYB)-S\d{3}$")
STRESS_MARKERS = ["urgent", "asap", "right now", "hurry", "panic", "help me", "!!", "??", "..."]

pytestmark = pytest.mark.skipif(
    not BASELINE_PATH.exists(), reason="baseline_questions.csv not written yet (Phase 3)"
)


def rows() -> list[dict]:
    with BASELINE_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def columns() -> list[str]:
    with BASELINE_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle).fieldnames or [])


def known_documents() -> dict[str, str]:
    known: dict[str, str] = {}
    for path in sorted(METADATA_DIR.glob("*_pilot_sources.csv")):
        with path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                doc_id = (row.get("document_id") or "").strip()
                if doc_id:
                    known[doc_id] = (row.get("domain") or "").strip()
    return known


def known_chunks() -> dict[str, dict]:
    chunks: dict[str, dict] = {}
    for path in sorted(CHUNK_DIR.glob("*_chunks.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                record = json.loads(line)
                chunks[record["chunk_id"]] = record
    return chunks


def test_columns_match_schema() -> None:
    assert columns() == REQUIRED_COLUMNS


def test_scenario_ids_are_unique_and_well_formed() -> None:
    ids = [r["scenario_id"] for r in rows()]
    duplicates = [i for i, n in Counter(ids).items() if n > 1]
    assert not duplicates, f"duplicate scenario_id: {duplicates}"
    malformed = [i for i in ids if not SCENARIO_ID.match(i)]
    assert not malformed, f"malformed scenario_id: {malformed}"


def test_domain_matches_scenario_prefix() -> None:
    for r in rows():
        prefix = r["scenario_id"].split("-")[0]
        assert DOMAINS[prefix] == r["domain"], f"{r['scenario_id']}: domain {r['domain']!r}"


def test_documents_exist_and_match_domain() -> None:
    known = known_documents()
    for r in rows():
        doc_id = r["document_id"]
        assert doc_id in known, f"{r['scenario_id']}: {doc_id} not in corpus/metadata"
        assert known[doc_id] == r["domain"], f"{r['scenario_id']}: domain mismatch for {doc_id}"


def test_evidence_chunks_exist_and_are_approved() -> None:
    """Section 7.3: every baseline question must point at approved evidence."""
    chunks = known_chunks()
    for r in rows():
        ids = json.loads(r["expected_retrieval_chunk_ids"])
        assert isinstance(ids, list) and ids, f"{r['scenario_id']}: empty evidence list"
        for chunk_id in ids:
            assert chunk_id in chunks, f"{r['scenario_id']}: chunk {chunk_id} does not exist"
            assert chunks[chunk_id]["quality_flag"] == "approved", (
                f"{r['scenario_id']}: chunk {chunk_id} is not approved"
            )
            assert chunks[chunk_id]["document_id"] == r["document_id"], (
                f"{r['scenario_id']}: chunk {chunk_id} belongs to another document"
            )


def test_text_fields_are_not_empty() -> None:
    for r in rows():
        for field in ("baseline_question", "ground_truth_context", "ground_truth_answer"):
            assert r[field].strip(), f"{r['scenario_id']}: {field} is empty"


def test_answer_does_not_exceed_evidence() -> None:
    """Section 8.4: the reference answer must not go beyond the evidence."""
    over = [
        r["scenario_id"]
        for r in rows()
        if len(r["ground_truth_answer"].split()) > len(r["ground_truth_context"].split())
    ]
    assert not over, f"answer longer than its evidence: {over}"


def test_questions_are_calm() -> None:
    """Section 8.4: baselines carry no stress markers; those belong to Phase 4."""
    flagged = []
    for r in rows():
        low = r["baseline_question"].lower()
        hits = [m for m in STRESS_MARKERS if m in low]
        if hits:
            flagged.append((r["scenario_id"], hits))
    assert not flagged, f"stress markers in baseline questions: {flagged}"


def test_all_questions_are_answerable() -> None:
    """Section 8.4 and the Phase 3 gate: every baseline must be answerable."""
    bad = [r["scenario_id"] for r in rows() if r["answerability_label"] != "yes"]
    assert not bad, f"answerability_label is not 'yes' for: {bad}"


def test_question_types_are_valid() -> None:
    for r in rows():
        assert r["question_type"] in QUESTION_TYPES, (
            f"{r['scenario_id']}: question_type {r['question_type']!r}"
        )


def test_thirty_questions_ten_per_domain() -> None:
    data = rows()
    assert len(data) == 30, f"{len(data)} questions; the pilot target is 30"
    per_domain = Counter(r["domain"] for r in data)
    for domain in DOMAINS.values():
        assert per_domain[domain] == 10, f"{domain}: {per_domain[domain]} questions, expected 10"


def test_question_type_distribution_is_not_badly_skewed() -> None:
    """Section 8.4: 'Distribusi taxonomy tidak terlalu timpang'."""
    data = rows()
    per_type = Counter(r["question_type"] for r in data)
    missing = QUESTION_TYPES - set(per_type)
    assert not missing, f"question types not represented: {sorted(missing)}"
    largest, count = per_type.most_common(1)[0]
    assert count / len(data) <= 0.40, (
        f"{largest} is {count}/{len(data)} of the set, which is badly skewed"
    )


def test_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR)], capture_output=True, text=True, cwd=REPO_ROOT
    )
    assert result.returncode == 0, f"validate_baselines.py failed:\n{result.stdout}"
