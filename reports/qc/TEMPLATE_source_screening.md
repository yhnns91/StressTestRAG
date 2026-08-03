# Source Screening — <DOMAIN>

- **Issue:** #NN
- **Branch:** `task/issue-NNN-<domain>-corpus-metadata`
- **Commit:** `<commit-hash>`
- **Date:** YYYY-MM-DD

---

## 1. Search strategy

Which official publishers were consulted, and what search terms were used.

-

## 2. Candidates evaluated

| # | Publisher | Title | URL | Decision |
|---|---|---|---|---|
| 1 | | | | ✅ include / ❌ exclude |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |

## 3. Included documents

### DOC-ID — <title>

- **Publisher:**
- **Why authoritative:**
- **Why stable:** (not a live alert, not fast-changing news)
- **Structure:** (headings and paragraphs suitable for chunking)
- **License status:** and how it was determined
- **Safety level:** and reasoning
- **Candidate topics for baseline questions:**

*(repeat for each included document)*

## 4. Excluded candidates

| Candidate | Reason for exclusion |
|---|---|
| | |

Common exclusion reasons: not an authoritative publisher; live alert or fast-changing news; content too broad for unambiguous questions; contains medical, self-harm, or exploitative material; redistribution status unresolvable.

## 5. Validation

```
$ python scripts/validate_metadata.py corpus/metadata/<DOMAIN>_pilot_sources.csv
<paste output>
```

## 6. Open questions

Items raised as `needs-review`, with issue numbers.

-
