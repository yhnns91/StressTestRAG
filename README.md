# StressTestRAG

**Human-Annotated Benchmark for Software Reliability Testing of Retrieval-Augmented Generation under Crisis-Induced Prompt Noise**

---

## What this is

A benchmark dataset for testing whether RAG pipelines degrade when users ask the same question under linguistic stress — anxiety, panic, urgency, fragmentation, typos, hostility.

Each **scenario** pairs one calm baseline question with five stressed variants that preserve the original semantic intent. Every question is linked to an evidence chunk from an official source document, so retrieval and grounding can be measured against a known ground truth.

**Framing:** software reliability testing for AI-NLP systems. This dataset is *not* a psychological assessment tool, *not* an emergency decision system, and *not* a source of operational safety instructions.

## Research question

> Do prompts that carry the same semantic intent, but exhibit crisis-induced linguistic noise, cause measurable degradation in retrieval quality, grounding, faithfulness, and answer relevance in a RAG pipeline?

## Domains

| Code | Domain | Scope |
|---|---|---|
| `DIS` | Natural disaster preparedness and response | Emergency kits, evacuation preparation, official warnings |
| `INF` | Infrastructure disruption and power outage | Generator safety, outage preparation, official channels |
| `CYB` | Non-exploitative cyber incident response | Reporting, containment principles, recovery guidance |

## Dataset targets

| Package | Baselines | Conditions | Total | Purpose |
|---|---|---|---|---|
| Pilot | 30 | 1 calm + 5 stressed | 180 | Validate guideline, agreement, QC, pipeline |
| Final | 120 | 1 calm + 5 stressed | 720 | Main release after pilot passes |

## Quick start

```bash
git clone <repository-url>
cd StressTestRAG

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
pytest -q
```

Validate the corpus metadata:

```bash
python scripts/validate_metadata.py corpus/metadata/INF_pilot_sources.csv
```

## Repository layout

```
data/raw_external_metadata/   Source metadata, URLs, checksums, access dates
data/interim/                 Intermediate working data
data/processed/               Cleaned, schema-conformant data
data/final/                   Release candidate and final dataset (QC-passed only)

corpus/metadata/              Document-level metadata CSV
corpus/extracted_text/        Extracted text that is legally storable
corpus/chunks/                Structured chunks with IDs and source trace

annotations/guideline/        Annotation guideline and codebook
annotations/pilot/            Raw annotation batches
annotations/adjudicated/      Final adjudicated labels

scripts/                      Runnable pipeline and validation scripts
src/                          Reusable modules
tests/                        Reproducibility tests
reports/                      QC, agreement, pilot RAG, and weekly reports
docs/                         Schema, datasheet, dataset card, ethics statement
```

## Working rules

1. **Order is locked.** Official corpus → chunks → evidence chunks → baseline questions → stress variants → annotation → QC → pilot RAG → release. No phase begins before the previous gate passes.
2. **Evidence first.** Ground-truth answers are written from an existing chunk, never from memory.
3. **No direct pushes to `main`.** All changes arrive through a pull request that closes an issue.
4. **When in doubt, stop.** Licensing, content safety, semantic drift, or ground-truth uncertainty → open an issue labelled `needs-review`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow.

## Excluded content

This dataset deliberately excludes diagnosis or medical emergency advice; self-harm and violence; cyber exploitation, malware, or offensive security steps; live alerts and fast-changing news; prompts that introduce facts, locations, casualties, or devices absent from the baseline evidence; and full text whose redistribution status is unclear.

## Status

| Phase | Description | Status |
|---|---|---|
| 0 | Setup and onboarding | 🔧 In progress |
| 1 | Reference corpus and metadata | ⬜ Not started |
| 2 | Chunking and ground-truth linking | ⬜ Not started |
| 3 | Baseline questions | ⬜ Not started |
| 4 | Stress prompt variants | ⬜ Not started |
| 5 | Human annotation and adjudication | ⬜ Not started |
| 6 | Quality control and dataset split | ⬜ Not started |
| 7 | Pilot RAG and statistical analysis | ⬜ Not started |
| 8 | Documentation and release | ⬜ Not started |

## License

Code: see `LICENSE`. Dataset licensing and redistribution limits are documented in `docs/dataset_card.md`.

Source documents remain the property of their publishers. Where redistribution rights are unclear, this repository stores metadata, URLs, checksums, and extraction scripts only.

## Citation

See `CITATION.cff`.
test
