#!/usr/bin/env python3
"""Extract plain text from the 12 pilot corpus documents (Phase 2, step 1).

Every document is extracted according to a rule declared in
configs/extraction_rules.json. Nothing is trimmed by hand: if a document needs a
page range or a section boundary, that boundary is declared in the config with a
reason, so the extraction can be reproduced and audited (assignment doc 3.2).

Output
------
corpus/extracted_text/<document_id>.txt   Page-separated plain text ("\\f" between
                                          PDF pages; HTML output is one block).
corpus/extracted_text/_manifest.json      What was extracted, how, and how much.

Usage
-----
    python scripts/extract_text.py
    python scripts/extract_text.py --only DIS-002
    python scripts/extract_text.py --source-root ~/Downloads/stresstest-sources
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "configs" / "extraction_rules.json"
OUTPUT_DIR = REPO_ROOT / "corpus" / "extracted_text"
PAGE_BREAK = "\f"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def die(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def normalise_whitespace(text: str) -> str:
    """Collapse runs of blank lines and strip trailing spaces, nothing else.

    Wording is never altered: source typos are part of the evidence and must
    survive into ground_truth_context unchanged.
    """
    lines = [line.rstrip() for line in text.splitlines()]
    out, blank = [], 0
    for line in lines:
        if line.strip():
            blank = 0
            out.append(line)
        else:
            blank += 1
            if blank <= 1:
                out.append("")
    return "\n".join(out).strip()


def slice_by_markers(text: str, start: str | None, end: str | None, doc_id: str) -> str:
    """Keep the span between the LAST occurrence of `start` and the next `end`.

    The last occurrence is used deliberately: headings such as "Appendix A" also
    appear in a table of contents, and the body section is the later one.
    """
    if start:
        idx = text.rfind(start)
        if idx < 0:
            die(f"{doc_id}: start_marker {start!r} not found in extracted text")
        text = text[idx:]
    if end:
        idx = text.find(end, 1)
        if idx < 0:
            print(f"  note: end_marker {end!r} not found; kept text to end of document")
        else:
            text = text[:idx]
    return text


# --------------------------------------------------------------------------- #
# extractors
# --------------------------------------------------------------------------- #
def extract_pdf(path: Path, rule: dict, doc_id: str) -> tuple[str, dict]:
    try:
        import pdfplumber
    except ImportError:
        die("pdfplumber is not installed. Run: pip install -r requirements.txt")

    scope = rule.get("scope", "full")
    pages_text: list[str] = []

    with pdfplumber.open(path) as pdf:
        total_pages = len(pdf.pages)
        if scope == "pages":
            first, last = rule["pages"]
            if not (1 <= first <= last <= total_pages):
                die(f"{doc_id}: page range {first}-{last} outside document (1-{total_pages})")
            selected = range(first - 1, last)
        else:
            selected = range(total_pages)

        for i in selected:
            # layout=True preserves reading order on multi-column pages, which
            # matters for the infographic-style hazard sheets.
            page_text = pdf.pages[i].extract_text(layout=True) or ""
            pages_text.append(page_text)

    text = PAGE_BREAK.join(pages_text)
    if scope == "markers":
        text = slice_by_markers(text, rule.get("start_marker"), rule.get("end_marker"), doc_id)

    info = {"total_pages": total_pages, "pages_extracted": len(pages_text)}
    return normalise_whitespace(text), info


def extract_html(path: Path, rule: dict, doc_id: str) -> tuple[str, dict]:
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        die("beautifulsoup4 is not installed. Run: pip install -r requirements.txt")

    raw = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw, "html.parser")

    dropped = 0
    for selector in rule.get("drop_selectors", []):
        for node in soup.select(selector):
            node.decompose()
            dropped += 1

    text = soup.get_text(separator="\n")
    text = re.sub(r"[ \t]+", " ", text)

    if rule.get("scope") == "markers":
        text = slice_by_markers(text, rule.get("start_marker"), rule.get("end_marker"), doc_id)

    info = {"elements_dropped": dropped}
    return normalise_whitespace(text), info


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> int:
    parser = argparse.ArgumentParser(description="Extract text from the pilot corpus documents.")
    parser.add_argument("--only", metavar="DOC_ID", help="extract a single document, e.g. DIS-002")
    parser.add_argument("--source-root", help="override source_root from the config")
    args = parser.parse_args()

    if not CONFIG_PATH.exists():
        die(f"config not found: {CONFIG_PATH}")
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    root = Path(args.source_root or config["source_root"]).expanduser()
    if not root.exists():
        die(f"source_root does not exist: {root}")

    documents = config["documents"]
    if args.only:
        if args.only not in documents:
            die(f"unknown document_id {args.only!r}. Known: {', '.join(sorted(documents))}")
        documents = {args.only: documents[args.only]}

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest, failures, needs_review = {}, [], []

    for doc_id in sorted(documents):
        rule = documents[doc_id]
        src = root / rule["file"]
        print(f"{doc_id}: {rule['file']}")

        if not src.exists():
            print(f"  MISSING: {src}")
            failures.append(doc_id)
            continue

        if rule["type"] == "pdf":
            text, info = extract_pdf(src, rule, doc_id)
        elif rule["type"] == "html":
            text, info = extract_html(src, rule, doc_id)
        else:
            die(f"{doc_id}: unknown type {rule['type']!r}")

        if not text.strip():
            print("  EMPTY OUTPUT -- check the extraction rule")
            failures.append(doc_id)
            continue

        out_path = OUTPUT_DIR / f"{doc_id}.txt"
        out_path.write_text(text, encoding="utf-8", newline="\n")

        words = len(text.split())
        print(f"  -> {out_path.relative_to(REPO_ROOT)}  ({words} words)")
        if rule.get("manual_review"):
            print("  MANUAL REVIEW REQUIRED: " + rule["reason"])
            needs_review.append(doc_id)

        manifest[doc_id] = {
            "source_file": rule["file"],
            "type": rule["type"],
            "scope": rule.get("scope", "full"),
            "reason": rule["reason"],
            "word_count": words,
            "manual_review": bool(rule.get("manual_review")),
            **info,
        }

    manifest_path = OUTPUT_DIR / "_manifest.json"
    manifest_path.write_text(
        json.dumps({"generated": date.today().isoformat(), "documents": manifest}, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    total_words = sum(d["word_count"] for d in manifest.values())
    print()
    print(f"Extracted {len(manifest)} document(s), {total_words} words total.")
    print(f"Manifest: {manifest_path.relative_to(REPO_ROOT)}")
    if needs_review:
        print(f"Manual review required: {', '.join(needs_review)}")
    if failures:
        print(f"FAILED: {', '.join(failures)}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
