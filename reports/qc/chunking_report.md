# Chunking and Ground-Truth Linking Report — Phase 2

- **Issue:** #14
- **Branch:** `task/issue-014-chunking-ground-truth`
- **Commit:** `9e9c041`
- **Date:** 2026-08-19

---

## 1. Summary

| Gate criterion (section 7, Gate Fase 2) | Target | Result |
|---|---|---|
| Valid chunks | about 100-150 | **124 approved** |
| Clear ground-truth candidate chunks | at least 30 | **32** |

129 chunks were produced from the twelve pilot documents; 124 are approved and 5
are rejected as page furniture. 33 ground-truth candidates were mapped onto 32
distinct evidence chunks and reviewed in two stages.

Four extraction defects were found and fixed during this phase. All four passed
every automated check that existed at the time and were only visible on reading
the text, which is discussed in section 6.

## 2. Pipeline

| Step | Script | Config | Output |
|---|---|---|---|
| Text extraction | `scripts/extract_text.py` | `configs/extraction_rules.json` | `corpus/extracted_text/*.txt` |
| Column-aware reading | `scripts/columns.py` | (called by the above) | — |
| Chunking | `scripts/build_chunks.py` | `configs/chunk_rules.json` | `corpus/chunks/*_chunks.jsonl` |
| Validation | `scripts/validate_chunks.py` | — | exit code |
| Tests | `tests/test_chunk_schema.py` | — | `pytest` |

Every deviation from a plain full-document extraction is declared in a config
file with a written reason rather than applied by hand, so the result is
reproducible and each exclusion is auditable (assignment section 3.2).

## 3. Extraction

### 3.1 Word counts

| Document | Words | Scope |
|---|---|---|
| CYB-001 | 2,952 | full |
| CYB-002 | 2,584 | pages 31-35, 41-43 (Appendices A, B, H) |
| CYB-003 | 2,295 | pages 29-33, 40-42 (Appendices A, B, H) |
| CYB-004 | 3,241 | pages 9-17 (Executive Summary, Sections 1-2) |
| DIS-001 | 525 | full |
| DIS-002 | 731 | full |
| DIS-003 | 535 | full |
| DIS-004 | 237 | `.cms-content` element only |
| INF-001 | 837 | full |
| INF-002 | 662 | full |
| INF-003 | 1,771 | article only, navigation stripped |
| INF-004 | 211 | body content only |
| **Total** | **16,581** | |

### 3.2 Scope limitations carried over from Phase 1

- **CYB-002 and CYB-003** are limited to Appendices A, B and H, following decision
  7.2 in the CYB screening report. The numbered chapters are fill-in template
  instructions. Marker-based slicing was tried first and abandoned: the word
  "Appendix" recurs throughout the body as cross-references, so it cannot be
  distinguished from a section heading. Page ranges verified by hand in a PDF
  viewer were used instead.
- **CYB-004** is limited to the Executive Summary and Sections 1-2. Section 3 is a
  CSF element reference table unsuitable for semantic chunking.

## 4. Chunking

Section 7.1 requires each chunk to hold one self-contained unit of meaning and
forbids merging separate procedures to reach a token target. Boundaries therefore
come from each document's own section headings, listed in `configs/chunk_rules.json`.
The token count is measured and reported, not used to force boundaries.

Headings are matched on their first occurrence only: strings such as "Appendix H"
and "Cybersecurity incident" recur later as cross-references and table cells, and
matching those would cut a document at points that are not section boundaries.

Where a heading is printed over two lines, the line to match and the label to
record differ: the FEMA sheets set "Prepare" above "NOW", recorded as "Prepare NOW".

### 4.1 Chunks per document

| Document | Chunks | Approved | Rejected | Tokens min/median/max |
|---|---|---|---|---|
| CYB-001 | 18 | 17 | 1 | 65 / 229 / 312 |
| CYB-002 | 22 | 21 | 1 | 5 / 114 / 318 |
| CYB-003 | 20 | 20 | 0 | 26 / 106 / 316 |
| CYB-004 | 21 | 20 | 1 | 24 / 191 / 321 |
| DIS-001 | 5 | 5 | 0 | 33 / 184 / 223 |
| DIS-002 | 5 | 5 | 0 | 94 / 248 / 248 |
| DIS-003 | 4 | 4 | 0 | 125 / 221 / 227 |
| DIS-004 | 5 | 5 | 0 | 23 / 43 / 84 |
| INF-001 | 7 | 7 | 0 | 21 / 126 / 279 |
| INF-002 | 5 | 5 | 0 | 63 / 220 / 233 |
| INF-003 | 15 | 14 | 1 | 3 / 172 / 265 |
| INF-004 | 2 | 1 | 1 | 86 / 171 / 171 |
| **Total** | **129** | **124** | **5** | |

### 4.2 Token range

The schema targets 180-320 tokens. Two kinds of documented deviation occur.

**Below 180.** Section 7.1 permits short checklists and FAQ entries to form
smaller chunks, and much of this corpus is exactly that. The four NWS flood alert
definitions run 23-84 tokens each and are the intended evidence for three
ground-truth candidates; a 180 token floor would discard them.

**Above 320.** One chunk, `CYB-004_C05` at 321 tokens, is a single list of attack
examples. Splitting it would divide one unit of meaning, which section 7.1
forbids, so it is kept whole with the reason recorded in its `note` field.

### 4.3 Rejected chunks

Five chunks are marked `rejected`. All are page furniture rather than guidance:

| Chunk | Content |
|---|---|
| `CYB-001_C01` | NCSC cover block and contents |
| `CYB-002_C01` | page footer, 5 tokens |
| `CYB-004_C01` | NIST running header |
| `INF-003_C01` | section title with no body, 3 tokens |
| `INF-004_C02` | DOE legal disclaimer |

Rejected chunks are kept in the files rather than deleted, so the decision stays
traceable. They are excluded from the valid chunk count and may not serve as
evidence.

### 4.4 Manual review of flagged chunks

The classifier's first pass flagged 10 rejected and 1 pending. Review found four
of those flags to be wrong, and the rules were corrected rather than the flags
edited by hand:

- **Minimum token floor lowered from 25 to 15.** At 25 it was rejecting the USDA
  rule "Never taste food to determine its safety. When In Doubt, Throw It Out!"
  (19 tokens) and the NWS page's own framing question (23 tokens). Both are
  self-contained units of meaning.
- **Template detection changed from any-line to majority-of-lines.** One
  "In your CIRP, include..." line appended to a real definition was enough to mark
  the whole chunk a template instruction, which put a wrong reason into the audit
  trail. `CYB-002_C02` and `CYB-002_C03` are definitions, not templates.
- **"Flooding Resources" removed from the non-evidence heading list.** Despite the
  navigational-sounding name, that section carries the question the whole NWS page
  answers.
- **Chunks above 320 tokens changed from `pending` to `approved`.** The decision is
  made and recorded in `note`; leaving it as `pending` implied it was still open.

## 5. Ground-truth linking

Section 7.3 requires the evidence chunk to be chosen and recorded before the
baseline question is written. `data/interim/ground_truth_candidates.csv` holds 33
candidates carried over from the Phase 1 screening reports, each mapped to the
chunk that answers it and given a factual summary drawn from that chunk.

### 5.1 Coverage

| Document | Distinct evidence chunks |
|---|---|
| CYB-001 | 3 |
| CYB-003 | 3 |
| CYB-004 | 4 |
| DIS-001 | 3 |
| DIS-002 | 2 |
| DIS-003 | 3 |
| DIS-004 | 4 |
| INF-001 | 2 |
| INF-002 | 3 |
| INF-003 | 4 |
| INF-004 | 1 |
| **Total** | **32** |

CYB-002 contributes no ground-truth chunks, following decision 7.1 in the CYB
screening report: it shares a document lineage with CYB-003, so CYB-003 is the
sole ground-truth source and CYB-002 is indexed as a near-duplicate distractor.

### 5.2 Question type distribution

| Type | Count |
|---|---|
| factual_information | 10 |
| procedural_guidance | 9 |
| misinformation_correction | 6 |
| clarification | 4 |
| resource_seeking | 3 |
| prioritization | 1 |

`prioritization` remains at one, as flagged in section 7.6 of the INF screening
report. Section 8.4 requires the taxonomy distribution not to be badly skewed, so
`prioritization`, `resource_seeking` and `clarification` should be targeted
deliberately when the 30 baseline questions are written in Phase 3.

### 5.3 Two-stage review

Both stages required by section 7.3 were carried out: evidence validity, then
chunk readability. All 33 candidates are `approved`. Six carry a review note.

Three candidates need two chunks each, because the answer spans a comparison:

| Candidate | Chunks | Reason |
|---|---|---|
| `CYB-S008` | `CYB-004_C09` + `C10` | C09 states the superseded view, C10 the correction |
| `DIS-S010` | `DIS-004_C03` + `C05` | Warning and Watch definitions are separate sections |
| `INF-S007` | `INF-003_C05` + `C06` | Unsafe and Safe-to-Eat lists are separate |

This is a pattern worth carrying into Phase 3: `clarification` and
`misinformation_correction` questions tend to need more than one evidence chunk,
because they ask about the relationship between two statements.

## 6. What the automated checks did not catch

Four extraction defects were found in this phase. Each passed the metadata
validator and the full test suite at the time it existed, and each was visible
only on reading the text.

### 6.1 CYB-002 and CYB-003 source files were swapped

**Found by** reading a page footer in the extracted text: the file named
`CYB-002_..._cirp...` carried the running header "Cybersecurity incident response
planning: Practitioner guidance". The terminology confirmed it — the December 2024
document says ASD, the older one says ACSC, and the two were the wrong way round.

**Impact.** Every checksum pointed at the wrong document. `publication_year`,
`publisher` and the licence basis recorded in Phase 1 all described the other file.

**Fixed** by swapping the filenames and the two checksums in
`corpus/metadata/CYB_pilot_sources.csv`. Commit `5deaee6`.

### 6.2 DIS-004 carried 140 words of site navigation

**Found by** mapping section headings and seeing HOME, FORECAST, Local, Graphical
and the rest of the weather.gov menu in the extracted text.

**Cause.** weather.gov contains no `<nav>`, `<header>`, `<footer>` or `<main>`
elements at all, so dropping by tag removed nothing.

**Fixed** by selecting the `.cms-content` element directly. Word count fell from
380 to 237, all of it article text.

### 6.3 Multi-column pages were read line by line across columns

**Found by** mapping section headings on the FEMA sheets. A line of the extracted
text read:

```
Secure items such as televisions and   Drop, Cover, and Hold On like you   Expect aftershocks to follow the
```

Those are the first lines of Prepare NOW, Survive DURING and Be Safe AFTER,
interleaved. A chunk built from that text would have mixed three separate
procedures, which section 7.1 forbids.

**Fixed** with `scripts/columns.py`, which detects columns from word coordinates
and reads each in turn. The key step is separating display-size headings before
measuring the column gaps: with them included, no vertical whitespace gap exists
and no columns are found. Where columns sit too close for automatic detection —
the CPSC alert, and page 3 of the NCSC guide — the boundary is given explicitly in
the config with its reason.

### 6.4 Three CYB-002 pages returned character-reversed text

**Found by** the same heading survey: pages 38-40 produced `xidneppA`, `etalpmeT`,
`retsigeR` — "Appendix", "Template", "Register" backwards. They are landscape
tables, and pdfplumber returned their character order reversed.

**Fixed** as a side effect of narrowing the scope to Appendices A, B and H, which
excludes those pages. Verified by `grep -l "xidneppA"` returning nothing.

### 6.5 The pattern

All four passed `validate_metadata.py` and the test suite. Word counts looked
plausible throughout. Section 7.4 calls its list "Pemeriksaan otomatis minimum" —
minimum — and this phase is a concrete illustration of why that word is there.

The chunk validator added in this phase (`scripts/validate_chunks.py`) closes part
of the gap. It was itself tested by injecting seven deliberate faults, all seven of
which it caught; that test also exposed a crash on relative paths, which was fixed.

## 7. Accepted limitations

### 7.1 DIS-002 retains a double text layer in its cover panel

The flood sheet stores two editions of its display text on top of one another, as
recorded in risk 7.1 of the DIS screening report. `DIS-002_C01` still contains the
interleaved result. The defect is confined to the cover panel; the page 2 prose,
from which all three DIS-002 ground-truth chunks are drawn, is unaffected.

### 7.2 INF-001_C01 is complete but fragmented

`INF-S002` asks which services a power outage may disrupt. All four impacts are
present in the chunk, but split across the cover panel layout, so the chunk reads
poorly even though every fact is there. Accepted as a known limitation of
infographic source documents rather than replaced. Section 12.6 frames this study
as measuring retriever sensitivity to query form; imperfect layout in real source
documents is part of the condition being tested, not a defect to hide.

### 7.3 Two chunks end with stray publisher text

`DIS-004_C02` ends with a notice about a change to Impact-Based warning format, and
`INF-002_C05` ends with a document code and phone number from the CPSC footer. Both
sit after the answer and do not affect it. Rebuilding the chunks to remove them
would shift every `chunk_id` and invalidate the ground-truth mapping, so they are
recorded rather than corrected.

### 7.4 INF-004 yields a single chunk

The DOE page has 211 words of body content, so its three ground-truth candidates
share one evidence chunk. Recorded in risk 7.3 of the INF screening report and
accepted there.

## 8. Schema change

Chunk records carry a `note` field that was not in `docs/schema.md`. It records why
a chunk was flagged, or why its token count sits outside 180-320 — section 7.4
requires a documented reason for such deviations, and this is where that reason
lives. Added to `docs/schema.md` section 2 and to `CHANGELOG.md` per section 4.3.
Commit `dae9d2c`.

`data/interim/ground_truth_candidates.csv` is a Phase 2 working file and is not in
the schema, which defines `data/interim/baseline_questions.csv` for Phase 3. Its
columns are `scenario_id`, `domain`, `document_id`, `expected_retrieval_chunk_ids`,
`candidate_question`, `question_type`, `ground_truth_summary`, `reviewer_status`
and `review_note`. It is expected to be superseded by the Phase 3 file rather than
maintained, so it is documented here instead of in the schema.

## 9. Validation

```
$ python scripts/validate_chunks.py
=== corpus\chunks\CYB_chunks.jsonl ===
  -> PASSED (0 error, 0 warning)
=== corpus\chunks\DIS_chunks.jsonl ===
  -> PASSED (0 error, 0 warning)
=== corpus\chunks\INF_chunks.jsonl ===
  -> PASSED (0 error, 0 warning)
Totals: 129 chunks | approved 124 | rejected 5

$ python scripts/validate_metadata.py corpus/metadata/CYB_pilot_sources.csv
  -> PASSED (0 warning)

$ python -m pytest -q
27 passed
```

The metadata validator now reports zero warnings for all three files. Every run
since Phase 1 had reported four per file for the empty `chunk_count` column; those
are now filled, which is what closes Phase 2's contribution to the metadata.

The test count rose from 12 to 27 with the addition of `tests/test_chunk_schema.py`.

## 10. Carried into Phase 3

- `prioritization` is represented once across 33 candidates and should be targeted
  deliberately (section 5.2 above, and section 7.6 of the INF screening report).
- Comparison questions need more than one evidence chunk (section 5.3).
- `expected_retrieval_chunk_ids` for all 33 candidates is already recorded, which is
  the ordering section 7.3 requires: evidence first, question second.
