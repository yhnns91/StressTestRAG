"""Column-aware page text extraction.

Multi-column infographic PDFs (the FEMA hazard sheets, the CPSC alert) place
several independent sections side by side. Reading such a page line by line
interleaves them: the first line of "Prepare NOW" is followed by the first line
of "Survive DURING" and then of "Be Safe AFTER". A chunk built from that text
would mix three unrelated procedures, which assignment section 7.1 forbids.

The fix is to detect the columns from word coordinates and read each one from
top to bottom in turn. Headings set in a larger face usually span the whole
width, so they are separated out before the column gaps are measured -- with
them included, no vertical whitespace gap exists and no columns are found.
"""

from __future__ import annotations

import statistics

LINE_TOLERANCE = 4.0     # points; words within this vertical distance share a line
MIN_COLUMN_GAP = 10      # points of empty width needed to call something a column break
HEADING_MARGIN = 0.6     # a word this much larger than the body size counts as a heading


def _bands(words, page_width: float, min_gap: int) -> list[tuple[int, int]]:
    """Return the x-ranges occupied by text, split wherever a wide gap appears."""
    covered = bytearray(int(page_width) + 2)
    for w in words:
        lo, hi = int(w["x0"]), min(int(w["x1"]) + 1, len(covered))
        for x in range(max(lo, 0), hi):
            covered[x] = 1
    bands, start, gap = [], None, 0
    for x, filled in enumerate(covered):
        if filled:
            if start is None:
                start = x
            gap = 0
        elif start is not None:
            gap += 1
            if gap >= min_gap:
                bands.append((start, x - gap))
                start, gap = None, 0
    if start is not None:
        bands.append((start, len(covered) - 1))
    return bands


def _render(words) -> str:
    """Join words into lines, reading top to bottom then left to right."""
    words = sorted(words, key=lambda w: (round(w["top"] / LINE_TOLERANCE), w["x0"]))
    lines, current, last_top = [], [], None
    for w in words:
        if last_top is not None and abs(w["top"] - last_top) > LINE_TOLERANCE:
            lines.append(" ".join(current))
            current = []
        current.append(w["text"])
        last_top = w["top"]
    if current:
        lines.append(" ".join(current))
    return "\n".join(lines)


def page_text(page, min_gap: int = MIN_COLUMN_GAP, splits: list[float] | None = None) -> str:
    """Extract one page, reading column by column when the page has columns.

    `splits` gives explicit x positions of the column gutters. Use it when the
    columns sit so close together that no measurable whitespace band exists --
    the CPSC alert is like this, and automatic detection returns a single column.
    """
    words = page.extract_words(extra_attrs=["size"])
    if not words:
        return ""

    body_size = statistics.median(w["size"] for w in words)
    body = [w for w in words if w["size"] <= body_size + HEADING_MARGIN]
    display = [w for w in words if w["size"] > body_size + HEADING_MARGIN]

    if splits:
        edges = [0.0, *splits, page.width]
        bands = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]
        parts = []
        if display:
            parts.append(_render(display))
        for lo, hi in bands:
            col = [w for w in body if lo <= (w["x0"] + w["x1"]) / 2 < hi]
            if col:
                parts.append(_render(col))
        return "\n".join(p for p in parts if p.strip())

    bands = _bands(body, page.width, min_gap) if body else []
    if len(bands) <= 1:
        # Single column: pdfplumber's own reading order is already correct.
        return page.extract_text() or ""

    parts = []
    if display:
        parts.append(_render(display))
    for lo, hi in bands:
        col = [w for w in body if w["x0"] < hi and w["x1"] > lo]
        if col:
            parts.append(_render(col))
    return "\n".join(p for p in parts if p.strip())
