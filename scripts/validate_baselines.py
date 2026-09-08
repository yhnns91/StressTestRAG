#!/usr/bin/env python3
"""Validate data/interim/baseline_questions.csv against docs/schema.md section 3
and the writing rules in assignment section 8.4.

Checks performed
----------------
Schema (docs/schema.md section 3)
  - the ten required columns are present, in order, with no extras
  - scenario_id matches [DOMAIN]-S[NNN] and is unique
  - domain is one of the three enum values and matches the scenario_id prefix
  - document_id exists in corpus/metadata and matches the domain
  - question_type is one of the six taxonomy values
  - answerability_label and reviewer_status use permitted values

Evidence link (assignment section 7.3 and 8.4)
  - expected_retrieval_chunk_ids is a non-empty JSON array
  - every chunk exists, is approved, and belongs to the stated document
  - ground_truth_context and ground_truth_answer are non-empty

Writing rules (assignment section 8.4)
  - baseline questions must be answerable: answerability_label = yes
  - questions must be calm: no stress markers, no shouting, no ellipsis
  - the reference answer must not be longer than the evidence it comes from

Exit code is 0 when everything passes and 1 when any error is found, so CI fails
on a broken baseline file.

Usage
-----
    python scripts/validate_baselines.py
    python scripts/validate_baselines.py data/interim/baseline_questions.csv
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATH = REPO_ROOT / "data" / "interim" / "baseline_questions.csv"
METADATA_DIR = REPO_ROOT / "corpus" / "metadata"
CHUNK_DIR = REPO_ROOT / "corpus" / "chunks"

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
ANSWERABILITY = {"yes", "partial", "no"}
REVIEWER_STATUS = {"pending", "approved", "revision_requested"}

SCENARIO_ID = re.compile(r"^(DIS|INF|CYB)-S\d{3}$")

# Section 8.4: a baseline question must be calm and complete, with no stress
# markers. Those belong to the stressed variants written in Phase 4.
STRESS_MARKERS = [
    "urgent", "urgently", "asap", "right now", "immediately!", "quick",
    "hurry", "panic", "help me", "please help", "!!", "??", "...",
]


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


def load_documents() -> dict[str, str]:
    """document_id -> domain, from the corpus metadata files."""
    known: dict[str, str] = {}
    for path in sorted(METADATA_DIR.glob("*_pilot_sources.csv")):
        with path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                doc_id = (row.get("document_id") or "").strip()
                if doc_id:
                    known[doc_id] = (row.get("domain") or "").strip()
    return known


def load_chunks() -> dict[str, dict]:
    chunks: dict[str, dict] = {}
    for path in sorted(CHUNK_DIR.glob("*_chunks.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                record = json.loads(line)
                chunks[record["chunk_id"]] = record
    return chunks


def validate(path: Path) -> Report:
    try:
        label = str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        label = str(path)
    rep = Report(label)

    documents = load_documents()
    chunks = load_chunks()
    if not documents:
        rep.error(label, "no document ids found in corpus/metadata")
        return rep
    if not chunks:
        rep.error(label, "no chunks found in corpus/chunks")
        return rep

    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = list(reader.fieldnames or [])
        rows = list(reader)

    if columns != REQUIRED_COLUMNS:
        missing = [c for c in REQUIRED_COLUMNS if c not in columns]
        extra = [c for c in columns if c not in REQUIRED_COLUMNS]
        if missing:
            rep.error(label, f"missing columns: {missing}")
        if extra:
            rep.error(label, f"unexpected columns: {extra}")
        if not missing and not extra:
            rep.warn(label, "columns are in a different order from docs/schema.md")

    seen_ids: set[str] = set()
    by_domain: Counter[str] = Counter()
    by_type: Counter[str] = Counter()
    evidence: set[str] = set()

    for number, row in enumerate(rows, start=2):
        scenario = (row.get("scenario_id") or "").strip()
        where = scenario or f"row {number}"

        # -- scenario_id ------------------------------------------------------
        if not SCENARIO_ID.match(scenario):
            rep.error(where, f"scenario_id {scenario!r} does not match [DOMAIN]-S[NNN]")
        if scenario in seen_ids:
            rep.error(where, "scenario_id is not unique")
        seen_ids.add(scenario)

        # -- domain -----------------------------------------------------------
        domain = (row.get("domain") or "").strip()
        prefix = scenario.split("-")[0] if "-" in scenario else ""
        if domain not in DOMAINS.values():
            rep.error(where, f"domain {domain!r} is not a permitted value")
        elif prefix in DOMAINS and DOMAINS[prefix] != domain:
            rep.error(where, f"domain {domain!r} does not match the scenario_id prefix {prefix}")
        by_domain[domain] += 1

        # -- document_id ------------------------------------------------------
        doc_id = (row.get("document_id") or "").strip()
        if doc_id not in documents:
            rep.error(where, f"document_id {doc_id!r} is not in corpus/metadata")
        elif documents[doc_id] != domain:
            rep.error(where, f"document {doc_id} belongs to domain {documents[doc_id]!r}")

        # -- evidence link (section 7.3) --------------------------------------
        raw_ids = (row.get("expected_retrieval_chunk_ids") or "").strip()
        try:
            chunk_ids = json.loads(raw_ids)
        except json.JSONDecodeError:
            rep.error(where, "expected_retrieval_chunk_ids is not valid JSON")
            chunk_ids = []
        if not isinstance(chunk_ids, list) or not chunk_ids:
            rep.error(where, "expected_retrieval_chunk_ids must be a non-empty JSON array")
            chunk_ids = []
        for chunk_id in chunk_ids:
            evidence.add(chunk_id)
            chunk = chunks.get(chunk_id)
            if chunk is None:
                rep.error(where, f"chunk {chunk_id} does not exist")
            elif chunk["quality_flag"] != "approved":
                rep.error(where, f"chunk {chunk_id} has quality_flag {chunk['quality_flag']!r}")
            elif chunk["document_id"] != doc_id:
                rep.error(where, f"chunk {chunk_id} belongs to {chunk['document_id']}, not {doc_id}")

        # -- text fields ------------------------------------------------------
        question = (row.get("baseline_question") or "").strip()
        context = (row.get("ground_truth_context") or "").strip()
        answer = (row.get("ground_truth_answer") or "").strip()
        if not question:
            rep.error(where, "baseline_question is empty")
        if not context:
            rep.error(where, "ground_truth_context is empty")
        if not answer:
            rep.error(where, "ground_truth_answer is empty")

        # Section 8.4: the reference answer must not exceed the evidence.
        if context and answer and len(answer.split()) > len(context.split()):
            rep.error(where, "ground_truth_answer is longer than ground_truth_context")

        # Section 8.4: baseline questions are calm, complete sentences.
        low = question.lower()
        hits = [m for m in STRESS_MARKERS if m in low]
        if hits:
            rep.error(where, f"baseline_question contains stress markers: {hits}")
        if question and not question.endswith("?"):
            rep.warn(where, "baseline_question does not end with a question mark")
        letters = [c for c in question if c.isalpha()]
        if letters and sum(c.isupper() for c in letters) / len(letters) > 0.5:
            rep.error(where, "baseline_question is mostly uppercase; baselines must be calm")

        # -- enums ------------------------------------------------------------
        q_type = (row.get("question_type") or "").strip()
        if q_type not in QUESTION_TYPES:
            rep.error(where, f"question_type {q_type!r} is not one of the six taxonomy values")
        by_type[q_type] += 1

        answerability = (row.get("answerability_label") or "").strip()
        if answerability not in ANSWERABILITY:
            rep.error(where, f"answerability_label {answerability!r} is not permitted")
        elif answerability != "yes":
            rep.error(where, "baseline questions must have answerability_label = yes (section 8.4)")

        status = (row.get("reviewer_status") or "").strip()
        if status not in REVIEWER_STATUS:
            rep.error(where, f"reviewer_status {status!r} is not permitted")

    # -- targets for the whole file -------------------------------------------
    if len(rows) != 30:
        rep.warn(label, f"{len(rows)} questions; the pilot target is 30 (section 8)")
    for domain in DOMAINS.values():
        if by_domain[domain] != 10:
            rep.warn(label, f"{domain}: {by_domain[domain]} questions; the target is 10 per domain")

    missing_types = QUESTION_TYPES - set(by_type)
    if missing_types:
        rep.warn(label, f"question types not represented: {sorted(missing_types)}")
    if rows:
        top = by_type.most_common(1)[0]
        if top[1] / len(rows) > 0.40:
            rep.warn(
                label,
                f"question type {top[0]!r} is {top[1]}/{len(rows)} of the set; "
                "section 8.4 asks for a distribution that is not badly skewed",
            )

    print(f"  questions: {len(rows)} | evidence chunks: {len(evidence)}")
    print("  per domain: " + ", ".join(f"{k.split('_')[0]} {v}" for k, v in sorted(by_domain.items())))
    print("  per type:   " + ", ".join(f"{k} {v}" for k, v in by_type.most_common()))
    return rep


def main() -> int:
    paths = [Path(a).resolve() for a in sys.argv[1:]] or [DEFAULT_PATH]
    failed = 0
    for path in paths:
        if not path.exists():
            print(f"ERROR: {path} does not exist", file=sys.stderr)
            failed += 1
            continue
        report = validate(path)
        report.print()
        if report.errors:
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
