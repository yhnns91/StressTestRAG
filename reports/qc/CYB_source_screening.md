# Source Screening — CYB

- **Issue:** #7
- **Branch:** `task/issue-007-cyber-corpus-metadata`
- **Commit:** `00bbabb`
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

### CYB-002 — Cyber Incident Response Plan Guidance

- **Publisher:** Australian Cyber Security Centre (ACSC), Australia — cyber.gov.au
- **Why authoritative:** The ACSC is Australia's national cyber security agency, part of
  the Australian Signals Directorate. The document is published on the cyber.gov.au domain
  as official agency guidance.
- **Why stable:** A standing planning template, not a live alert or news item. The document
  carries no printed publication date; 2022 was inferred from the title of Appendix K,
  "ACSC Incident Categorisation Matrix 2022". The URL path folder (2023-03) was not used as
  the basis, since ACSC folder years reflect upload date rather than publication date — a
  point demonstrated by CYB-003, which sits in a 2025-10 folder despite being dated
  December 2024. The document is superseded in substance by CYB-003 but remains published.
- **Structure:** 56 pages, approximately 10,713 words. Fourteen numbered chapters followed
  by Appendices A-K. The document is a fill-in template rather than narrative guidance:
  39 passages take the form "Include information about...", several appendices are blank
  tables, and the worked examples are marked "demonstrative only, and should not be used as
  the basis of your CIRP". Only Appendices A (terminology), B (readiness checklist) and
  H (post-incident review) consist of usable prose.
- **License status:** CC BY 4.0. No licence statement appears anywhere inside the PDF; the
  status was determined from https://www.cyber.gov.au/about-us/copyright, which states that
  ACSC material is released under a Creative Commons Attribution 4.0 International licence.
  The source of this determination is recorded in the metadata `notes` column, since it is
  external to the document itself.
- **Safety level:** `medium`. The schema defines `medium` as "contains procedural detail
  that must be quoted carefully". The document covers notification and reporting
  obligations to ASD and the OAIC, where an incorrectly grounded answer could lead an
  organisation to miss a regulatory duty, and it sets out evidence handling procedures
  where careless quotation could compromise the evidential value of collected material.
- **Role in the dataset:** No candidate baseline questions are drawn from this document.
  Under decision 7.1, CYB-003 is the sole ground-truth source for the ACSC material.
  CYB-002 is chunked and indexed so that it functions as a realistic near-duplicate
  distractor during retrieval, but no expected_retrieval_chunk_ids will reference it.

### CYB-003 — Cybersecurity incident response planning: Practitioner guidance

- **Publisher:** Australian Signals Directorate (ASD) / Australian Cyber Security Centre,
  Australia — cyber.gov.au
- **Why authoritative:** The ASD is Australia's national signals intelligence and cyber
  security agency, and the ACSC operates within it. The document is published on the
  cyber.gov.au domain as official agency guidance.
- **Why stable:** A standing planning guide, not a live alert or news item. The document
  records two dates on its cover: first published January 2022, last updated December 2024.
  The December 2024 version is the one downloaded and checksummed. It is the current
  revision of the ACSC incident response planning material and cites ISO/IEC 27035-1:2023
  and 27035-2:2023.
- **Structure:** 51 pages, approximately 9,510 words. Fourteen numbered chapters followed
  by Appendices A-K. The numbered chapters are largely fill-in template instructions — 30
  passages take the form "Include information about..." — and Appendices D, E, F, G and I
  are blank tables. Appendices A (terminology and definitions), B (readiness checklist) and
  H (post cybersecurity incident reviews) consist of usable prose with clear headings, and
  the document's scope is limited to those three appendices for chunking purposes.
- **License status:** CC BY 4.0, stated on the final page of the document: "© Commonwealth
  of Australia 2024 ... provided under a Creative Commons Attribution 4.0 International
  licence". Redistribution is permitted with attribution, so the record is marked
  `open_license_redistributable` and full text may be stored.
- **Safety level:** `medium`. The schema defines `medium` as "contains procedural detail
  that must be quoted carefully". The document covers notification and reporting
  obligations to ASD and the OAIC, where an incorrectly grounded answer could lead an
  organisation to miss a regulatory duty, and it sets out evidence handling procedures
  where careless quotation could compromise the evidential value of collected material.
  The same value is assigned to CYB-002, since the two documents share this content.
- **Role in the dataset:** Under decision 7.1, this document is the sole ground-truth
  source for the ACSC material.
- **Candidate baseline questions:**
  1. What is the difference between a hot debrief and a formal debrief?
     — evidence: p.41, Appendix H "Step 1 - Hold cybersecurity incident debriefs"
     — type: clarification
  2. How does the guidance define a cybersecurity incident?
     — evidence: p.31, Appendix A "Terminology and definitions"
     — type: factual_information
  3. Which questions could a facilitator use to guide discussion during a hot debrief?
     — evidence: p.41, Appendix H "Hot debrief guidance - Content"
     — type: procedural_guidance

### CYB-004 — Incident Response Recommendations and Considerations for Cybersecurity Risk Management (NIST SP 800-61r3)

- **Publisher:** National Institute of Standards and Technology (NIST), U.S. Department of
  Commerce — nvlpubs.nist.gov
- **Why authoritative:** NIST is the US federal standards body for cybersecurity guidance.
  The document is a numbered Special Publication with a registered DOI
  (10.6028/NIST.SP.800-61r3), published through the official NIST publications repository.
- **Why stable:** A standards publication, not a live alert or news item. Dated April 2025
  and carrying a formal revision identifier. It supersedes SP 800-61r2, which was withdrawn
  in April 2025 and rejected during this screening for that reason.
- **Structure:** 48 pages, approximately 14,196 words. Only the Executive Summary and
  Sections 1-2 (PDF pages 9-17) consist of prose. Section 3 is a CSF element reference
  table whose rows follow a fixed "CSF Element / Description / Priority / Recommendations"
  format, with many cells containing only cross-references such as "N1: See the notes for
  PR."; that structure does not preserve a self-contained unit of meaning and is unsuitable
  for semantic chunking. The remainder is references, acronyms, glossary and change log.
  The document's scope is therefore limited to PDF pages 9-17.
- **License status:** Public domain. The document states that it "is not subject to
  copyright in the United States", adding that attribution is appreciated by NIST. As a US
  Government work there is no redistribution restriction, so the record is marked
  `public_domain` and full text may be stored.
- **Safety level:** `low`. The schema defines `low` as "general guidance, no sensitive
  detail". The publication explicitly removed procedural content: Section 1.1 states that
  "the details of how to perform incident response activities change so often and vary so
  much across technologies, environments, and organizations, it is no longer feasible to
  capture and maintain that information in a single static publication". A keyword check
  found `exploit` and `persistence` used only descriptively, for example "eradication may
  be necessary to eliminate persistence mechanisms", with no technical steps given.
- **Candidate baseline questions:**
  1. What reason does the publication give for no longer providing detailed incident
     response procedures?
     — evidence: p.11, Section 1.1 "Purpose and Scope"
     — type: factual_information
  2. Is incident response best handled as a separate set of activities performed by a
     separate team?
     — evidence: p.12, Section 2.1 "Incident Response Life Cycle Model"
     — type: misinformation_correction
  3. Which of the six CSF 2.0 Functions support preparation rather than incident response
     itself?
     — evidence: p.13, Section 2.1 "Incident Response Life Cycle Model"
     — type: clarification


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
