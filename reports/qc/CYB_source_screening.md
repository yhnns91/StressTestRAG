# Source Screening — CYB

- **Issue:** #7
- **Branch:** `task/issue-007-cyber-corpus-metadata`
- **Commit:** `<hasil langkah 2>`
- **Date:** 2026-08-13

---

## 1. Search strategy

Which official publishers were consulted, and what search terms were used.

-

## 2. Candidates evaluated

| # | Publisher | Title | URL | Decision |
|---|---|---|---|---|
| 1 | NCSC | Cyber Security Small Business Guide: Response and Recovery | https://www.ncsc.gov.uk/sites/default/files/documents/NCSC_A5%20Response%20and%20Recovery%20Guide_v3_OCT20.pdf | ✅ include |
| 2 | ACSC | Cyber Incident Response Plan Guidance | https://www.cyber.gov.au/sites/default/files/2023-03/ACSC%20Cyber%20Incident%20Response%20Plan%20Guidance_A4.pdf | ✅ include |
| 3 | ASD | Cybersecurity incident response planning: Practitioner guidance | https://www.cyber.gov.au/sites/default/files/2025-10/Cybersecurity%20incident%20response%20planning%20-%20Practitioner%20guidance%20%28December%202024%29.pdf | ✅ include |
| 4 | NIST | Incident Response Recommendations and Considerations for Cybersecurity Risk Management | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf | ✅ include |
| 5 | NIST | Computer Security Incident Handling Guide (SP 800-61 Rev. 2) | csrc.nist.gov | ❌ exclude |
| 6 | CISA | Reporting a Cyber Incident | cisa.gov | ❌ exclude |
| 7 | CISA | CIRCIA | cisa.gov | ❌ exclude |

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
| NIST SP 800-61 Rev. 2 | Withdrawn 3 April 2025 and superseded by r3; fails the stability criterion |
| CISA — Reporting a Cyber Incident | Almost entirely a link list; insufficient prose for 180-320 token chunks; scoped to Emergency Communications Centers |
| CISA — CIRCIA | Regulatory page still under active rulemaking; fails the stability criterion |

Common exclusion reasons: not an authoritative publisher; live alert or fast-changing news; content too broad for unambiguous questions; contains medical, self-harm, or exploitative material; redistribution status unresolvable.

## 5. Validation

```
$ python scripts/validate_metadata.py corpus/metadata/CYB_pilot_sources.csv
=== corpus\metadata\CYB_pilot_sources.csv ===
  WARN   row 2: chunk_count is empty (acceptable before Phase 2)
  WARN   row 3: chunk_count is empty (acceptable before Phase 2)
  WARN   row 4: chunk_count is empty (acceptable before Phase 2)
  WARN   row 5: chunk_count is empty (acceptable before Phase 2)
  -> PASSED (4 warning)

$ pytest -q
10 passed, 2 skipped in 0.74s
```

## 6. Open questions

Items raised as `needs-review`, with issue numbers.

-
