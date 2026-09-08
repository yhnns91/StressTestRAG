# Baseline Questions Report — Phase 3

- **Issue:** #16
- **Branch:** `task/issue-016-baseline-questions`
- **Commit:** `74ff595`
- **Date:** 2026-08-21

---

## 1. Summary

| Gate criterion (section 8, Gate Fase 3) | Target | Result |
|---|---|---|
| Baseline questions written | 30 | **30** |
| Every question has an expected chunk | all | **all 30** |
| `answerability_label` | `yes` for all | **yes for all 30** |
| Accepted by review without substantive change | at least 95% | **29/30 = 96.7%** |

Thirty calm baseline questions were written against 32 approved evidence chunks,
ten per domain. Reviewer verification read every question against its chunk and
found two mislabelled question types; one required the question to be replaced,
the other only a label correction.

## 2. What was produced

| File | Contents |
|---|---|
| `data/interim/baseline_questions.csv` | 30 questions, ten columns per `docs/schema.md` section 3 |
| `scripts/validate_baselines.py` | Schema, evidence-link and section 8.4 writing checks |
| `tests/test_baseline_schema.py` | 12 tests; total suite rose from 27 to 40 |

## 3. Selection

### 3.1 Starting point

Phase 2 left 33 ground-truth candidates in
`data/interim/ground_truth_candidates.csv`, each already mapped to an approved
evidence chunk and passed through the two-stage review required by section 7.3.
Phase 3 needed 30, ten per domain, so the set had to be adjusted rather than
copied.

### 3.2 The imbalance to fix

| Domain | Candidates from Phase 2 | Target |
|---|---|---|
| CYB | 9 | 10 |
| DIS | 12 | 10 |
| INF | 12 | 10 |

Cyber was one short while the other two were two over, so the change was not a
simple removal of three.

Section 5.3 of the chunking report also recorded that `prioritization` appeared
once across the 33 candidates while `factual_information` and
`procedural_guidance` together accounted for more than half. Section 8.4 requires
that the taxonomy distribution not be badly skewed, so the selection was used to
improve it.

### 3.3 What was removed and why

| Candidate | Type | Reason |
|---|---|---|
| `CYB-S001` | factual_information | `factual` was the most over-represented type in CYB |
| `DIS-S006` | misinformation_correction | Shared chunk `DIS-002_C03` with `DIS-S005` |
| `DIS-S011` | factual_information | DIS-004 contributed four candidates, the most of any DIS document |
| `INF-S002` | factual_information | Chunk `INF-001_C01` is complete but fragmented (chunking report 7.2) |
| `INF-S011` | factual_information | Shared chunk `INF-004_C01` with two other candidates |
| `INF-S012` | procedural_guidance | Shared chunk `INF-004_C01`; removal leaves one candidate on that chunk |

Four of the six were removed because they shared an evidence chunk with another
candidate. Removing them raises the number of distinct chunks exercised per
question without losing topic coverage.

### 3.4 What was added and why

Three questions were written from chunks that Phase 2 had not used, out of the
92 approved chunks that were still untouched.

| New question | Chunk | Type |
|---|---|---|
| `CYB-S010` — Which threats should a small organisation prepare for first? | `CYB-001_C05` | prioritization |
| `CYB-S011` — Where does the guide suggest looking for advice when trying to identify a cyber incident? | `CYB-001_C13` | resource_seeking |
| `INF-S013` — Which foods and utensils should be discarded after floodwater has entered a home? | `INF-003_C10` | procedural_guidance |

Four other chunks were examined and rejected during this search. They are
recorded here because the reasons matter for later phases:

| Chunk | Why rejected |
|---|---|
| `CYB-001_C07` | Begins mid-sentence: the bullet list it opens with continues from the previous chunk, so it does not stand alone as evidence despite passing every automated check |
| `CYB-001_C09` | Its high keyword score came from two long URLs, not from content about ordering or priority |
| `CYB-001_C10` | Refers to cyber insurance and trade associations, which are not official information channels under section 2.1 |
| `INF-001_C03` | Contains "Learn the signs of carbon monoxide poisoning" and "Talk to your doctor", passages already excluded in the INF-001 metadata notes under section 2.3 |

`CYB-002_C18` was also considered and set aside: it is a good passage, but
CYB-002 is not a ground-truth source under decision 7.1 of the CYB screening
report.

### 3.5 Final distribution

| Domain | Questions |
|---|---|
| cyber_incident_response | 10 |
| natural_disaster | 10 |
| infrastructure_disruption | 10 |

| Question type | Count | Share |
|---|---|---|
| procedural_guidance | 9 | 30% |
| factual_information | 6 | 20% |
| misinformation_correction | 5 | 17% |
| resource_seeking | 4 | 13% |
| clarification | 4 | 13% |
| prioritization | 2 | 7% |

All six taxonomy types are represented and no type exceeds 30%.

## 4. Writing the reference answers

Two columns did not exist in the Phase 2 candidate file and were written here:
`ground_truth_context` and `ground_truth_answer`.

Section 8.4 requires the reference answer to be concise, factual, and not to
exceed the evidence. `ground_truth_context` quotes the passage the answer is
drawn from, so that the relationship between the two can be checked directly
rather than inferred.

The validator enforces the rule by word count, and it caught a violation in the
first draft: `INF-S001` had a 16-word answer against a 12-word context, because
the context had been written as a single short sentence. The context was widened
to the surrounding passage in the same chunk, giving 42 words.

## 5. Reviewer verification

Every question was read against its evidence chunk and checked against three
questions that automated tests cannot answer:

- Is the answer actually present in this chunk?
- Does answering require anything from outside the chunk?
- Does the question introduce a place, time, casualty, brand or condition that
  the document does not contain (section 8.4)?

### 5.1 Result

| Outcome | Count |
|---|---|
| Accepted with no change at all | 28 |
| Substantive change (question replaced) | 1 |
| Label correction only (question, evidence and answer unchanged) | 1 |

**Acceptance rate against the gate: 29/30 = 96.7%.** The gate wording is
"accepted by review without substantive change"; the `INF-S013` correction
changed only the `question_type` column, leaving the question, its evidence and
its answer untouched. Both corrections are reported here rather than folded
together, so the distinction can be judged rather than taken on trust.

### 5.2 The two corrections

**`CYB-S011` — substantive.** The question was *"When should staff and customers
be informed after a cyber incident?"*, labelled `resource_seeking`. Section 8.1
defines that type as seeking an official channel, with the example "Where should
official outage updates be checked?". The question asked *when*, not *through
which channel*, so the label did not fit the content. Rather than relabel it, the
question was replaced with one drawn from `CYB-001_C13`, a chunk that genuinely
names where to look for advice. The replacement was then verified against its
chunk in the same way as the rest.

**`INF-S013` — label only.** The question asks which foods and utensils to
discard after a flood, which is a list rather than an order of actions. Section
8.1 defines `prioritization` as asking about a safe sequence. The label was
corrected to `procedural_guidance`; nothing else changed.

The second correction is worth stating plainly: the question had been labelled
`prioritization` in order to raise the count for that type. That is the wrong way
round. The label must follow the content of the question, not the shape of the
distribution.

## 6. Accepted limitations

### 6.1 `prioritization` has only two questions

After the corrections, `prioritization` accounts for 2 of 30 questions
(`CYB-S010` and `DIS-S007`).

This is a property of the corpus rather than an oversight. Of the 124 approved
chunks, only two contain a genuine ordering of actions: the tornado sheet's cover
panel, which ranks shelter locations in descending order of preference, and the
NCSC preparation passage, which says to plan for the most likely incidents rather
than every possible one. The remaining chunks hold definitions, rules and lists.

Every untouched CYB chunk was read while searching for a third. None contained an
ordering. The alternative was to mislabel a list question as `prioritization`,
which is what the `INF-S013` correction above removed.

Section 13.3 permits a reduced count where it is explained scientifically. The
explanation here is that the source documents are guidance sheets and reference
publications, which state what to do rather than what to do first.

**Consequence for Phase 7.** Analysis is paired per `scenario_id`. With two
scenarios, `prioritization` cannot support a claim about how that question type
behaves under stress. It should either be reported as under-powered or excluded
from per-type comparisons.

### 6.2 Two questions share one evidence chunk

`INF-S001` and `INF-S003` both point at `INF-001_C05`. The chunk carries two
distinct instructions — never use a gas appliance to heat a home, and do not run
a vehicle in a garage — so both questions remain answerable from it. The pairing
is recorded because in Phase 7 the two scenarios will exercise the same chunk.

### 6.3 Wingdings bullets in ACSC chunks

Some CYB-003 chunks contain the character U+F0A7, a Wingdings bullet carried over
from the source PDF. The data is stored correctly as UTF-8 and retrieval operates
on tokens rather than glyphs, but printing such a chunk to a Windows terminal
raises `UnicodeEncodeError` unless the output encoding is set explicitly. This
surfaced while generating the review listing for this phase.

Annotators in Phase 5 will see a replacement glyph for these bullets. Whether to
strip them from the chunk text or keep them as part of the source wording is left
open; keeping them preserves fidelity to the source, which section 8.4 requires
for `ground_truth_context`.

### 6.4 `INF-002_C05` ends with a page footer

The chunk used for `INF-S006` ends with `5123/0407/RV0917 638-2772 •
www.cpsc.gov`. The footer sits after the answer and does not affect it. Recorded
in section 7.3 of the chunking report.

## 7. Validation

```
$ python scripts/validate_baselines.py
  questions: 30 | evidence chunks: 32
  per domain: cyber 10, infrastructure 10, natural 10
  per type:   procedural_guidance 9, factual_information 6,
              misinformation_correction 5, resource_seeking 4,
              clarification 4, prioritization 2
=== data\interim\baseline_questions.csv ===
  -> PASSED (0 error, 0 warning)

$ python -m pytest -q
40 passed
```

`scripts/validate_baselines.py` implements the schema constraints from
`docs/schema.md` section 3 and the writing rules from section 8.4:

| Check | Rule |
|---|---|
| Column set and order | docs/schema.md section 3 |
| `scenario_id` format and uniqueness | `[DOMAIN]-S[NNN]` |
| `domain` matches the scenario prefix and the document's own domain | section 4.1 ID conventions |
| Evidence chunks exist, are `approved`, and belong to the stated document | section 7.3 |
| `ground_truth_answer` is not longer than `ground_truth_context` | section 8.4 |
| No stress markers, no mostly-uppercase questions | section 8.4 |
| `answerability_label = yes` | section 8.4 and the Phase 3 gate |
| Question type distribution warning above 40% | section 8.4 |

The test count rose from 27 to 40 with `tests/test_baseline_schema.py`.

## 8. Carried into Phase 4

- **Five stressed variants per baseline**, giving 30 x 6 = 180 pilot samples
  (section 9.2).
- **`prioritization` is under-powered at two scenarios** (section 6.1 above).
  Phase 7 should treat per-type comparisons for that type with caution.
- **Comparison questions use two evidence chunks.** `CYB-S008`, `DIS-S010` and
  `INF-S007` each point at two chunks because the answer spans a contrast. The
  stressed variants for these three must preserve both halves of the comparison,
  or the evidence link breaks.
- **`expected_retrieval_chunk_ids` is already recorded for all 30 questions**, so
  section 9.4's requirement that stressed variants keep the expected evidence
  relevant can be checked directly against this file.
