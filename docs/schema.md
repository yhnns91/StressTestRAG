# Data Schema

Every schema change must be recorded in `CHANGELOG.md` and reflected here.

---

## 1. Corpus metadata

**Location:** `corpus/metadata/<DOMAIN>_pilot_sources.csv`
**Format:** CSV, UTF-8
**Validator:** `python scripts/validate_metadata.py <file>`

| Column | Type | Required | Description |
|---|---|:---:|---|
| `document_id` | string | ✅ | `[DIS\|INF\|CYB]-NNN`, e.g. `INF-001`. Unique across all files. |
| `domain` | enum | ✅ | `natural_disaster`, `infrastructure_disruption`, `cyber_incident_response`. Must match the ID prefix. |
| `source_type` | string | ✅ | e.g. `official_guidance`, `government_factsheet`, `agency_checklist` |
| `document_title` | string | ✅ | Title as published |
| `publication_year` | int | ✅ | Between 1990 and the current year |
| `source_url` | string | ✅ | Full URL including scheme. Unique. |
| `publisher` | string | ✅ | Issuing organisation |
| `license_status` | enum | ✅ | See table below |
| `safety_level` | enum | ✅ | `low`, `medium`, `high` |
| `document_length` | int | ⬜ | Character or word count. May be blank before Phase 2. |
| `chunk_count` | int | ⬜ | Filled in during Phase 2. |
| `download_date` | date | ✅ | `YYYY-MM-DD`, not in the future |
| `checksum` | string | ✅ | SHA-256 hex digest, 64 characters. Use `scripts/compute_checksum.py`. |
| `notes` | string | ⬜ | Required when `license_status = excluded` (record the reason). |

### `license_status` values

| Value | Meaning | What may be stored |
|---|---|---|
| `public_domain` | No copyright restriction | Full text |
| `open_license_redistributable` | Open licence permitting redistribution | Full text + licence note |
| `metadata_only_until_verified` | Status not yet confirmed | Metadata, URL, checksum, extraction script only |
| `metadata_only_restricted` | Redistribution confirmed not permitted | Metadata, URL, checksum, extraction script only |
| `excluded` | Rejected during screening | Nothing beyond the metadata row and the reason |

> **Default to caution.** When redistribution rights are unclear, use `metadata_only_until_verified` and open a `needs-review` issue. Never store full text on the assumption that it is probably fine.

### `safety_level` values

| Value | Meaning |
|---|---|
| `low` | General guidance, no sensitive detail |
| `medium` | Contains procedural detail that must be quoted carefully |
| `high` | Borderline — requires explicit review before inclusion |

---

## 2. Chunk records

**Location:** `corpus/chunks/<DOMAIN>_chunks.jsonl`
**Format:** JSONL (one JSON object per line)
**Phase:** 2

```json
{
  "chunk_id": "INF-001_C03",
  "document_id": "INF-001",
  "heading": "Generator Safety",
  "text": "Use generators outdoors and away from windows...",
  "token_count": 216,
  "paragraph_index": 7,
  "source_url": "https://example.gov/outage-safety",
  "quality_flag": "approved"
}
```

| Field | Type | Description |
|---|---|---|
| `chunk_id` | string | `<document_id>_C<NN>`. Unique. |
| `document_id` | string | Must exist in the corpus metadata. |
| `heading` | string | Section heading the chunk belongs to. |
| `text` | string | Chunk content. Must not be empty. |
| `token_count` | int | Target 180–320. Deviations require a documented reason. |
| `paragraph_index` | int | Position within the document, for source trace. |
| `source_url` | string | Inherited from the document. |
| `quality_flag` | enum | `approved`, `pending`, `rejected` |

---

## 3. Baseline questions

**Location:** `data/interim/baseline_questions.csv`
**Phase:** 3

| Column | Description |
|---|---|
| `scenario_id` | `[DOMAIN]-S[NNN]`, e.g. `INF-S012` |
| `domain` | Same enum as corpus metadata |
| `document_id` | Source document |
| `expected_retrieval_chunk_ids` | JSON array of chunk IDs, e.g. `["INF-001_C03"]` |
| `baseline_question` | Calm, complete, stress-free phrasing |
| `ground_truth_context` | The evidence text the answer is drawn from |
| `ground_truth_answer` | Concise, factual, never exceeding the evidence |
| `question_type` | `factual_information`, `procedural_guidance`, `clarification`, `resource_seeking`, `prioritization`, `misinformation_correction` |
| `answerability_label` | `yes`, `partial`, `no` — baselines must be `yes` |
| `reviewer_status` | `pending`, `approved`, `revision_requested` |

---

## 4. Final dataset

**Location:** `data/final/`
**Format:** CSV + JSONL
**Phase:** 6 onward

Required columns:

```
sample_id, domain, scenario_id, document_id, chunk_id,
baseline_question, stressed_prompt,
stress_category, stress_intensity, emotional_tone, urgency_level,
linguistic_noise_type, clarity_score, semantic_equivalence_score,
answerability_label, safety_sensitivity_label,
ground_truth_context, ground_truth_answer, expected_retrieval_chunk_ids,
annotator_1_label, annotator_2_label, adjudicated_label, agreement_score,
split_type, creation_method, quality_flag
```

### Stress categories

| Category | Default intensity |
|---|:---:|
| `calm` | 0 |
| `anxious` | 1 |
| `panicked` | 3 |
| `angry_frustrated` | 2 |
| `cognitively_overloaded` | 3 |
| `fragmented_telegraphic` | 2 |
| `typo_heavy_informal` | 2 |
| `urgent_time_pressured` | 3 |
| `distrustful_hostile` | 2 |

---

## 5. ID conventions

| Object | Format | Example |
|---|---|---|
| Document | `[DOMAIN]-[3 digit]` | `DIS-001` |
| Chunk | `[document_id]_C[2 digit]` | `DIS-001_C03` |
| Scenario | `[DOMAIN]-S[3 digit]` | `INF-S012` |
| Sample | `STR-[6 digit]` | `STR-000184` |
| Annotation batch | `ANN-[YYYYMMDD]-B[2 digit]` | `ANN-20260805-B01` |

## 6. Versioning

| Tag | Meaning |
|---|---|
| `v0.1.0` | Pilot dataset (180 samples) |
| `v0.9.0` | Release candidate |
| `v1.0.0` | Public release |
