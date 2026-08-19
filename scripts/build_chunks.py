#!/usr/bin/env python3
"""Build semantic chunks from the extracted corpus text (Phase 2, step 2).

Boundaries come from each document's own section headings, listed in
configs/chunk_rules.json. Assignment section 7.1 requires a chunk to hold one
self-contained unit of meaning and forbids merging separate procedures to reach a
token target, so the heading structure decides where chunks begin and end. The
token count is measured and reported, not used to force boundaries.

Output
------
corpus/chunks/<DOMAIN>_chunks.jsonl   One JSON object per line, per docs/schema.md
corpus/chunks/_summary.json           Counts per document, for the chunking report

Usage
-----
    python scripts/build_chunks.py
    python scripts/build_chunks.py --only DIS-001
    python scripts/build_chunks.py --report        # print the table, write nothing
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHUNK_RULES = REPO_ROOT / "configs" / "chunk_rules.json"
TEXT_DIR = REPO_ROOT / "corpus" / "extracted_text"
METADATA_DIR = REPO_ROOT / "corpus" / "metadata"
CHUNK_DIR = REPO_ROOT / "corpus" / "chunks"


def die(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


# --------------------------------------------------------------------------- #
# token counting
# --------------------------------------------------------------------------- #
_encoder = None


def count_tokens(text: str) -> int:
    """Count tokens with tiktoken, falling back to a word-based estimate.

    The count is written into the chunk record so that validate_chunks.py and the
    CI job never need tiktoken, which downloads its encoding on first use.
    """
    global _encoder
    if _encoder is None:
        try:
            import tiktoken

            _encoder = tiktoken.get_encoding("cl100k_base")
        except Exception:  # offline, or tiktoken unavailable
            _encoder = False
    if _encoder is False:
        return int(len(text.split()) / 0.75)
    return len(_encoder.encode(text))


# --------------------------------------------------------------------------- #
# loading
# --------------------------------------------------------------------------- #
def load_metadata() -> dict[str, dict]:
    """Read document_id -> row from the three corpus metadata files."""
    rows: dict[str, dict] = {}
    for path in sorted(METADATA_DIR.glob("*_pilot_sources.csv")):
        with path.open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                if row.get("document_id"):
                    rows[row["document_id"]] = row
    if not rows:
        die(f"no metadata rows found under {METADATA_DIR}")
    return rows


def normalise(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip()


# --------------------------------------------------------------------------- #
# chunking
# --------------------------------------------------------------------------- #
def split_sections(text: str, headings: list, preamble: str) -> list[tuple[str, str]]:
    """Cut the document at its headings. Returns [(heading, body), ...].

    A heading entry is either a plain string, or an object with `match` (the
    exact line to look for) and `label` (what to record). The two differ when a
    heading is printed over two lines: the FEMA sheets set "Prepare" above "NOW",
    so the line to match is "Prepare" while the meaningful label is "Prepare NOW".

    Each heading matches its FIRST occurrence only. These strings recur later as
    cross-references and table cells, and matching those would cut the document
    at points that are not section boundaries.
    """
    wanted = {}
    for h in headings:
        match = h["match"] if isinstance(h, dict) else h
        label = h.get("label", match) if isinstance(h, dict) else h
        wanted[normalise(match).lower()] = normalise(label)

    sections: list[tuple[str, list[str]]] = [(preamble, [])]
    for raw in text.replace("\f", "\n").splitlines():
        line = normalise(raw)
        key = line.lower()
        if key in wanted:
            sections.append((wanted.pop(key), []))   # pop: first occurrence only
        else:
            sections[-1][1].append(line)             # blank lines kept as separators
    return [(h, "\n".join(b).strip()) for h, b in sections if "\n".join(b).strip()]


ITEM_END = re.compile(r"[.!?:;]$|\)$")


def to_items(body: str) -> list[str]:
    """Reflow wrapped lines into whole items.

    PDF extraction breaks each line at the printed line width, so a single
    recommendation arrives as four or five fragments and there are no blank lines
    to mark where the next one starts. An item is treated as complete when its
    last line ends in sentence punctuation; the following line opens a new one.
    """
    items, current = [], []
    for line in body.splitlines():
        line = line.strip()
        if not line:
            if current:
                items.append(" ".join(current))
                current = []
            continue
        current.append(line)
        if ITEM_END.search(line):
            items.append(" ".join(current))
            current = []
    if current:
        items.append(" ".join(current))
    return [i for i in items if i.strip()]


def split_long(body: str, max_tokens: int, target: int) -> list[str]:
    """Divide an over-long section between whole items, never inside one.

    A section that holds only one item is returned whole: section 7.1 prefers an
    oversized chunk to one unit of meaning cut in half. The deviation is recorded
    on the chunk instead.
    """
    if count_tokens(body) <= max_tokens:
        return [body]
    items = to_items(body)
    if len(items) < 2:
        return [body]
    out, current = [], []
    for item in items:
        candidate = "\n".join(current + [item])
        if current and count_tokens(candidate) > target:
            out.append("\n".join(current))
            current = [item]
        else:
            current.append(item)
    if current:
        out.append("\n".join(current))
    return out


def is_template(text: str, markers: list[str]) -> bool:
    """True when the text is an instruction to the reader rather than a fact."""
    low = text.lower()
    hits = sum(1 for m in markers if m in low)
    if not hits:
        return False
    # One marker inside a long passage is a passing remark; a short passage built
    # around such a phrase is a template instruction.
    return hits >= 2 or len(text.split()) < 90


def build(doc_id: str, meta: dict, rule: dict, cfg: dict) -> list[dict]:
    path = TEXT_DIR / f"{doc_id}.txt"
    if not path.exists():
        die(f"{doc_id}: extracted text not found at {path}. Run extract_text.py first.")
    text = path.read_text(encoding="utf-8")

    max_tokens = cfg["max_tokens"]
    min_tokens = cfg["min_tokens"]
    markers = cfg["template_markers"]

    chunks: list[dict] = []
    for para_index, (heading, body) in enumerate(
        split_sections(text, rule["headings"], rule["preamble_heading"]), start=1
    ):
        for piece in split_long(body, max_tokens, cfg["target_tokens"]):
            tokens = count_tokens(piece)
            if is_template(piece, markers):
                flag, note = "rejected", "template instruction, not answerable evidence"
            elif heading.lower() in cfg.get("non_evidence_headings", []):
                flag, note = "rejected", "publisher footer or navigation, not corpus content"
            elif tokens < min_tokens:
                flag, note = "rejected", f"fragment below {min_tokens} tokens"
            elif tokens > max_tokens:
                flag, note = "pending", "single item above 320 tokens, kept whole (section 7.1)"
            elif tokens < 180:
                flag, note = "approved", "short section; section 7.1 permits smaller chunks"
            else:
                flag, note = "approved", ""
            chunks.append(
                {
                    "chunk_id": f"{doc_id}_C{len(chunks) + 1:02d}",
                    "document_id": doc_id,
                    "heading": heading,
                    "text": piece,
                    "token_count": tokens,
                    "paragraph_index": para_index,
                    "source_url": meta["source_url"],
                    "quality_flag": flag,
                    "note": note,
                }
            )
    return chunks


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description="Build chunks from extracted corpus text.")
    ap.add_argument("--only", metavar="DOC_ID", help="build one document only")
    ap.add_argument("--report", action="store_true", help="print the summary without writing files")
    args = ap.parse_args()

    if not CHUNK_RULES.exists():
        die(f"config not found: {CHUNK_RULES}")
    config = json.loads(CHUNK_RULES.read_text(encoding="utf-8"))
    cfg, rules = config["chunking"], config["documents"]
    metadata = load_metadata()

    targets = [args.only] if args.only else sorted(rules)
    if args.only and args.only not in rules:
        die(f"unknown document_id {args.only!r}")

    by_domain: dict[str, list[dict]] = {}
    summary: dict[str, dict] = {}

    print(f"{'doc':<9} {'chunks':>7} {'approved':>9} {'pending':>8} {'rejected':>9}  {'tokens min/med/max':>20}")
    print("-" * 70)
    for doc_id in targets:
        if doc_id not in metadata:
            die(f"{doc_id} is in chunk_rules.json but not in the corpus metadata")
        chunks = build(doc_id, metadata[doc_id], rules[doc_id], cfg)
        flags = Counter(c["quality_flag"] for c in chunks)
        toks = sorted(c["token_count"] for c in chunks) or [0]
        med = toks[len(toks) // 2]
        print(
            f"{doc_id:<9} {len(chunks):>7} {flags['approved']:>9} {flags['pending']:>8} "
            f"{flags['rejected']:>9}  {toks[0]:>6}/{med}/{toks[-1]}"
        )
        by_domain.setdefault(doc_id.split("-")[0], []).extend(chunks)
        summary[doc_id] = {
            "chunks": len(chunks),
            "approved": flags["approved"],
            "pending": flags["pending"],
            "rejected": flags["rejected"],
            "token_min": toks[0],
            "token_median": med,
            "token_max": toks[-1],
        }

    total = sum(s["chunks"] for s in summary.values())
    approved = sum(s["approved"] for s in summary.values())
    pending = sum(s["pending"] for s in summary.values())
    rejected = sum(s["rejected"] for s in summary.values())
    print("-" * 70)
    print(f"{'TOTAL':<9} {total:>7} {approved:>9} {pending:>8} {rejected:>9}")
    print()
    print(f"Valid chunks (approved): {approved}   Phase 2 gate target: about 100-150")

    if args.report:
        print("\n--report given: no files written.")
        return 0

    CHUNK_DIR.mkdir(parents=True, exist_ok=True)
    for domain, chunks in sorted(by_domain.items()):
        out = CHUNK_DIR / f"{domain}_chunks.jsonl"
        with out.open("w", encoding="utf-8", newline="\n") as fh:
            for c in chunks:
                fh.write(json.dumps(c, ensure_ascii=False) + "\n")
        print(f"  wrote {out.relative_to(REPO_ROOT)}  ({len(chunks)} chunks)")

    (CHUNK_DIR / "_summary.json").write_text(
        json.dumps(
            {
                "generated": date.today().isoformat(),
                "totals": {"chunks": total, "approved": approved, "pending": pending, "rejected": rejected},
                "documents": summary,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"  wrote {(CHUNK_DIR / '_summary.json').relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
