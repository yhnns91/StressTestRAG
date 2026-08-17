# Source Screening — CYB

- **Issue:** #7
- **Branch:** `task/issue-007-cyber-corpus-metadata`
- **Commit:** `322cea1`
- **Date:** 2026-08-13

---


## 1. Search strategy

**Publishers consulted.** Screening was restricted to national cyber security
agencies and standards bodies, on the grounds that their publications are stable,
authored under a clear institutional mandate, and issued in English. Four were
searched directly: the National Cyber Security Centre (UK), the Australian Cyber
Security Centre and Australian Signals Directorate (Australia), the National
Institute of Standards and Technology (US), and the Cybersecurity and
Infrastructure Security Agency (US). ENISA and CERT/CC were held in reserve in
case fewer than four documents met the criteria.

**Search terms used.** Search terms were not recorded at the time and could not be recovered from browser history. Publisher sites were browsed directly rather than through general search.

**Sources deliberately not used.** Blogs, vendor whitepapers, discussion forums
and news articles were excluded on principle rather than case by case, even where
they were easier to read. Section 6.7 of the assignment document identifies
reliance on such sources as a common failure, and none of them satisfies the
requirement for an identifiable publishing authority or for content stability
over time.

**Scope constraint applied throughout.** Only non-exploitative incident response
material was considered. Documents covering offensive technique, malware
analysis, credential handling or deep forensic procedure were out of scope by
design, in line with Section 2.3.


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

### CYB-001 — Cyber Security Small Business Guide: Response and Recovery

- **Publisher:** National Cyber Security Centre (NCSC), United Kingdom — ncsc.gov.uk
- **Why authoritative:** NCSC is the UK's national cyber security authority. The guide is
  published on the ncsc.gov.uk domain as official guidance, not as third-party commentary
  or opinion.
- **Why stable:** A standing guide, not a live alert or news item. Published October 2020
  and still actively maintained — the content was updated in April 2026 when Action Fraud
  references were removed. Note that the publisher replaced the file in place without
  changing the URL or filename (still v3_OCT20), so checksum and download_date are the only
  reliable version markers.
- **Structure:** 12 pages, approximately 2,938 words. Introduction, then Step 1 through
  Step 5, then Resources. Each step carries its own heading and stands on its own, which
  suits semantic chunking. The document exceeds the 2-10 page screening range, but was
  accepted because its word count is modest and its section boundaries are unambiguous.
- **License status:** Open Government Licence, stated on the final page of the document
  (p. 12). OGL permits redistribution with attribution, so the record is marked
  `open_license_redistributable` and full text may be stored.
- **Safety level:** `low`. The schema defines `low` as "general guidance, no sensitive
  detail". The content is entirely general advice with no technical procedures. A keyword
  check for `exploit`, `persistence`, `forensic` and `memory image` returned zero
  occurrences — the only one of the four documents with no matches at all.
- **Candidate baseline questions:**
  1. What signs might indicate that a cyber incident has occurred?
     — evidence: p.7, Step 2 "Find out if you are being (or have been) attacked"
     — type: factual_information
  2. Which channels does the guide recommend for reporting a cyber attack to
     law enforcement?
     — evidence: p.10, Step 4 "Report to law enforcement"
     — type: resource_seeking
  3. What actions may be required when an organisation that manages its own IT
     activates its incident plan?
     — evidence: p.9, Step 3 "If you manage your own IT: put your plan into action"
     — type: procedural_guidance


## 4. Excluded candidates

| Candidate | Reason for exclusion |
|---|---|
| NIST SP 800-61 Rev. 2 | Withdrawn 3 April 2025 and superseded by r3; fails the stability criterion |
| CISA — Reporting a Cyber Incident | Almost entirely a link list; insufficient prose for 180-320 token chunks; scoped to Emergency Communications Centers |
| CISA — CIRCIA | Regulatory page still under active rulemaking; fails the stability criterion |



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

- **CYB-002 licence — resolved, no issue raised.** The PDF carries no licence
  statement. Verified against https://www.cyber.gov.au/about-us/copyright, which
  states CC BY 4.0 for ACSC material. Recorded as `open_license_redistributable`,
  with the source of the determination noted in the metadata `notes` column.
- **Validator encoding bug — resolved.** `test_validator_passes` failed on Windows
  because non-ASCII characters in the validator output could not be encoded to the
  cp1252 pipe used by `subprocess`. Fixed by replacing them with ASCII equivalents.
- No `needs-review` issues are open for this batch.


## 7. Accepted risks

Three issues were identified during screening. All four candidates were retained in
the corpus, but the handling of each issue changed how those documents are used;
the reasoning is recorded below.

### 7.1 CYB-002 and CYB-003 share a document lineage

**Condition.** The two ACSC documents are not independent sources. CYB-003 is a
later revision of the same underlying guidance as CYB-002.

**Evidence.** Both follow an identical section sequence and both carry the same
Appendix A-K structure. A literal comparison of consecutive 8-word sequences found
2,119 exact matches, roughly 23% of the shorter document; 125 blocks of 15
consecutive identical words were also found. By comparison, the same measure
between CYB-004 and CYB-001 returned zero. CYB-002 cites NIST SP 800-61 Revision 2
and the ACSC Annual Cyber Threat Report 2021, while CYB-003 cites ISO/IEC
27035-1:2023 and 27035-2:2023 and was last updated December 2024. Critically, the
overlap is concentrated in Appendices A, B and H — the only sections of either
document that consist of usable prose.

**Impact.** Two consequences follow. First, Phase 6 near-duplicate detection
(11.1, item 3) will flag chunk pairs drawn from these documents. Second and more
seriously, if the same statement appears in chunks from both documents, a
retriever returning the chunk that is not listed in expected_retrieval_chunk_ids
is not semantically wrong, yet Context Precision would score it as a failure. That
would degrade the validity of the calm-vs-stressed measurement, which is the core
of the study.

**Options considered.** (a) retain only one document and replace the other from
the ENISA or CERT/CC reserve; (b) retain both and restrict ground-truth selection
to non-overlapping sections; (c) retain both and treat the overlap as a documented
dataset limitation; (d) retain both in the corpus but designate one as the sole
ground-truth source.

**Decision.** Option (d). CYB-003 is the sole ground-truth source for the ACSC
material; no expected_retrieval_chunk_ids will reference a CYB-002 chunk. CYB-002
is still chunked and indexed, where it functions as a realistic near-duplicate
distractor of the kind a production retrieval corpus contains. Option (b) was
rejected once the overlap was found to sit precisely in the prose appendices, so
the non-overlapping remainder is template instruction that cannot serve as
evidence in any case. CYB-003 was chosen over CYB-002 because it is the current
revision and cites current standards. The consequence — four cyber documents but
three ground-truth sources — is accepted and recorded here.

### 7.2 Three documents exceed the 2-10 page screening range

**Condition.** CYB-002 (56 pages), CYB-003 (51 pages) and CYB-004 (48 pages) are
substantially longer than the range set for this screening.

**Evidence.** Estimated at 250 tokens per chunk, the four documents would together
yield roughly 200 chunks, against a Phase 2 pilot target of 100-150 chunks for all
twelve corpus documents.

**Impact.** Left unbounded, the cyber domain alone would consume the entire chunk
budget, leaving the disaster and infrastructure domains underrepresented and
skewing domain coverage in the final dataset.

**Options considered.** (a) restrict each long document to a defined prose
section; (b) accept the full documents and reduce chunk counts elsewhere; (c)
replace the long documents with shorter ones.

**Decision.** Option (a). CYB-004 is limited to the Executive Summary and Sections
1-2 (printed pages 1-9); Section 3 is a CSF element reference table unsuitable for
semantic chunking and the remainder is references, acronyms and glossary. CYB-003
is limited to Appendix A (terminology), Appendix B (readiness checklist) and
Appendix H (post-incident review), which are the prose sections; the numbered
chapters preceding them are template instructions. CYB-002 needs no scope limit,
since under 7.1 it contributes no ground-truth chunks.

### 7.3 Much of CYB-002 and CYB-003 is template instruction, not evidence

**Condition.** Both ACSC documents are response plan templates rather than
narrative guidance.

**Evidence.** CYB-002 contains 39 passages of the form "Include information
about..." and CYB-003 contains 30. Appendices D, E, F, G and I are blank tables
(situation report, incident log, evidence register, remediation plan, action
register), and CYB-002 marks its worked examples as "demonstrative only, and
should not be used as the basis of your CIRP".

**Impact.** A sentence instructing the reader to supply their own content cannot
answer a question, so it cannot serve as a ground-truth chunk. The usable evidence
in both documents is therefore narrower than the page count suggests.

**Options considered.** (a) select ground-truth chunks only from prose sections
and mark template passages as quality_flag = rejected during Phase 2; (b) exclude
both documents.

**Decision.** Option (a). Chunks whose text is a template instruction or a blank
table will carry quality_flag = rejected, a value already defined in the chunk
schema, so they remain traceable rather than being silently dropped.
