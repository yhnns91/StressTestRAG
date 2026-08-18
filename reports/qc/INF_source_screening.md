# Source Screening — INF

- **Issue:** #12
- **Branch:** `task/issue-012-infrastructure-corpus-metadata`
- **Commit:** `<isi sebelum push terakhir>`
- **Date:** 2026-08-18

---

> Page references in this section use PDF viewer page numbers. For the two HTML
> sources, references name the section heading instead.

## 1. Search strategy

**Publishers consulted.** Screening was restricted to federal agencies with a direct
statutory role in the subject matter, rather than to general preparedness portals. Four
were searched: the Federal Emergency Management Agency through its Ready Campaign
(ready.gov), the U.S. Consumer Product Safety Commission (cpsc.gov), the USDA Food Safety
and Inspection Service (fsis.usda.gov), and the Department of Energy's Office of
Cybersecurity, Energy Security, and Emergency Response (energy.gov/ceser).

**Search terms used.**
- ready.gov power outage hazard information sheet PDF
- USDA FSIS food safety during power outage refrigerator freezer fact sheet
- CPSC portable generator carbon monoxide safety alert PDF
- energy.gov power outage preparedness stay informed official updates

Searching was carried out with assistant support; the terms above are the ones that
produced the accepted candidates.

**Selection principle: one agency per topic.** Section 2.1 lists four example topics for
this domain — generator safety, outage preparation, official information channels, and
food and device safety. Rather than take four documents from one publisher, one document
was selected per topic from the agency that owns that subject matter: FEMA for outage
preparation, CPSC for consumer product hazards, FSIS for food safety, and DOE for energy
emergency information. This is the main reason literal overlap in this batch is zero.

**Lessons applied from earlier batches.** Document length was checked before download, as
in the DIS batch. Candidates from the same publisher were compared against each other
before selection, following the CYB-002/CYB-003 experience; this is what led to the second
CPSC document being evaluated and rejected rather than accepted alongside the first.

**Sources deliberately not used.** State and county emergency management pages, utility
company pages and commercial energy portals appeared repeatedly in search results and were
excluded as a class: they are not federal-level authorities, and several carried live
outage data that changes every few minutes.

## 2. Candidates evaluated

| # | Publisher | Title | URL | Decision |
|---|---|---|---|---|
| 1 | FEMA | Be Prepared for a Power Outage (V-1008) | https://www.ready.gov/sites/default/files/2024-03/ready.gov_power-outage_hazard-info-sheet.pdf | include |
| 2 | CPSC | Portable Generator Hazards, Safety Alert 5123 | https://www.cpsc.gov/s3fs-public/Portable_Generator_Safety_Alert_2017_5123.pdf | include |
| 3 | USDA FSIS | Keep Your Food Safe During Emergencies | https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/emergencies/keep-your-food-safe-during-emergencies | include |
| 4 | DOE CESER | Staying Informed | https://www.energy.gov/ceser/staying-informed | include |
| 5 | CPSC | What to Know About Generators and CO (468) | https://www.cpsc.gov/s3fs-public/468-WhattoKnowGenerators_2022.pdf | exclude |
| 6 | FDA | Food and Water Safety During Power Outages and Floods | https://www.fda.gov/food/buy-store-serve-safe-food/food-and-water-safety-during-power-outages-and-floods | exclude |
| 7 | FEMA / Ready | Power Outages (HTML page) | https://www.ready.gov/power-outages | exclude |

## 3. Included documents

### INF-001 — Be Prepared for a Power Outage (FEMA V-1008)

- **Publisher:** Federal Emergency Management Agency, U.S. Department of Homeland
  Security — ready.gov
- **Why authoritative:** FEMA is the US federal emergency management agency. The sheet
  carries the FEMA seal and an official publication number, distributed through the
  agency's Ready Campaign site.
- **Why stable:** A standing preparedness sheet, not a live alert. Dated December 2023 on
  the cover, and covered by the publisher's statement at ready.gov/publications that these
  publications are current as of 30 September 2025 and will not be updated on a regular
  basis thereafter.
- **Structure:** 2 pages, approximately 837 words. Page 1 is a cover panel with a
  definition, four impact icons and seven protective actions. Page 2 carries Prepare NOW,
  Survive DURING and Be Safe AFTER, plus a closing block on concurrent disasters. The same
  three-section layout as the DIS hazard sheets, which gives clean chunk boundaries.
- **License status:** `open_license_redistributable`, on the same basis as the DIS FEMA
  sheets: no licence statement inside the PDF, status determined from the Reprint Terms of
  Use at ready.gov/publications, which require that content not be altered and that use not
  imply FEMA endorsement.
- **Safety level:** `medium`. The sheet carries specific numeric thresholds (a refrigerator
  holds about 4 hours, a full freezer about 48 hours, generators at least 20 feet from
  building openings) where a misquoted figure would be directly hazardous.
- **Note on excluded passages:** the sheet advises learning the signs of carbon monoxide
  poisoning, describes them as flu-like, and recommends talking to a doctor about medical
  devices and medication storage. Section 2.3 excludes medical advice, so ground-truth
  chunks are not drawn from those passages.
- **Candidate baseline questions:**
  1. Is it safe to use a gas stove or oven to heat a home during a power outage?
     — evidence: p.2, "Survive DURING"
     — type: misinformation_correction
  2. What services may a power outage disrupt?
     — evidence: p.1, cover panel impact icons
     — type: factual_information
  3. What precautions apply when using a vehicle as a source of power or warmth during an
     outage?
     — evidence: p.2, "Survive DURING"
     — type: procedural_guidance

### INF-002 — Portable Generator Hazards (CPSC Safety Alert 5123)

- **Publisher:** U.S. Consumer Product Safety Commission — cpsc.gov
- **Why authoritative:** The CPSC is the US federal agency responsible for consumer product
  safety and is the body that collects the incident data cited in the document. The alert
  carries the CPSC seal and the agency's contact details.
- **Why stable:** A standing safety alert, not a news item. The footer code 5123/0407/RV0917
  records an original issue of April 2007 and a revision of September 2017, and the document
  has not been revised since.
- **Structure:** 1 page, approximately 672 words. Four clearly headed blocks — an
  introduction naming the hazard categories, then Carbon Monoxide Hazards, Electrical
  Hazards and Fire Hazards. Each block is self-contained prose with bulleted detail.
- **License status:** `open_license_redistributable`. The CPSC Privacy and Security Notice
  states that web page text, brochures and posters on CPSC websites are public information
  that may be freely distributed, copied or linked to, provided the use does not state or
  imply CPSC endorsement and CPSC is credited. `public_domain` was not used because CPSC
  says "public information" rather than "public domain" and attaches those two conditions.
  The same notice warns that images may be licensed from stock providers; only text is
  stored, so that restriction does not apply here.
- **Safety level:** `medium`. The document is entirely procedural safety detail covering
  three distinct hazard categories, including the backfeeding prohibition, where a
  misquoted instruction could be fatal to the reader or to a utility worker.
- **Candidate baseline questions:**
  1. What are the primary hazards to avoid when using a portable generator?
     — evidence: p.1, opening paragraph
     — type: factual_information
  2. Is it safe to power house wiring by plugging a generator into a wall outlet?
     — evidence: p.1, "Electrical Hazards"
     — type: misinformation_correction
  3. How should fuel for a generator be stored?
     — evidence: p.1, "Fire Hazards"
     — type: procedural_guidance

### INF-003 — Keep Your Food Safe During Emergencies (USDA FSIS)

- **Publisher:** USDA Food Safety and Inspection Service — fsis.usda.gov
- **Why authoritative:** FSIS is the USDA agency responsible for food safety regulation in
  the United States, and this page is its own guidance rather than a restatement of another
  agency's material. FDA and FoodSafety.gov versions of the same advice were evaluated and
  rejected as derivative.
- **Why stable:** The page footer records "Last Updated: Aug 07, 2013". It has not been
  revised in thirteen years, which makes it the most stable item in the corpus. The
  corollary is that the guidance may lag current practice; that is acceptable here because
  the dataset measures retrieval reliability rather than publishing food safety advice, and
  the point is recorded in the metadata notes.
- **Structure:** HTML page, approximately 1,782 words of article content. Organised as Plan
  Ahead, During a Power Outage, After a Power Outage, then Refrigerated Foods and Frozen
  Foods with explicit Unsafe Foods and Safe-to-Eat Foods lists. See section 7.2 for an
  extraction hazard.
- **License status:** `public_domain`. The FSIS Policies and Links page states that
  information presented on the FSIS website is in the public domain, that information in
  FSIS fact sheets or on the website is considered public information which may be
  distributed or copied, and that authorisation to reprint is granted, with source credit
  requested. The request for credit is a courtesy rather than a condition, so unlike CPSC
  this qualifies as public domain under the schema definition.
- **Safety level:** `medium`. The page carries specific temperature and time thresholds and
  itemised discard lists. A misquoted threshold could lead to foodborne illness.
- **Candidate baseline questions:**
  1. What is the difference between refrigerated foods that must be discarded after a power
     outage and those that remain safe to eat?
     — evidence: "After a Power Outage — Refrigerated Foods", Unsafe Foods and Safe-to-Eat
       Foods lists
     — type: clarification
  2. Should perishable food be placed outside in the snow during a winter power outage?
     — evidence: "During a Power Outage"
     — type: misinformation_correction
  3. What should be done in advance so that stored food stays safe if the power fails?
     — evidence: "Power Outages — Plan Ahead"
     — type: procedural_guidance

### INF-004 — Staying Informed (DOE CESER)

- **Publisher:** U.S. Department of Energy, Office of Cybersecurity, Energy Security, and
  Emergency Response — energy.gov
- **Why authoritative:** CESER is the DOE office responsible for energy sector emergency
  response. The page sits within the office's Energy Security section on the energy.gov
  domain.
- **Why stable:** Page metadata records `article:published_time` of 30 May 2013 and
  `article:modified_time` of 25 September 2023. The content is advisory rather than
  time-sensitive and has not been revised in almost three years.
- **Structure:** HTML page, 211 words of body content: an opening line and five bullets,
  followed by a disclaimer. This is the shortest item in the corpus and is expected to yield
  approximately one chunk. Section 7.1 of the assignment document permits short checklists
  to have smaller chunks, so this is within the rules, but the three candidate questions
  below will share a single evidence chunk rather than pointing to three distinct ones.
- **License status:** `public_domain`. The DOE Web Policies page states that government
  information at DOE websites is in the public domain and may be freely distributed and
  copied, with acknowledgement of the Department of Energy requested.
- **Safety level:** `low`. The page identifies where to obtain information and does not
  instruct the reader to take any physical action.
- **Note on excluded passages:** the final two bullets refer readers to social media
  platforms and to commercial services (AAA, GasBuddy). Section 2.3 excludes forums,
  opinion and sources without clear authority, so ground-truth chunks are drawn only from
  the first three bullets.
- **Candidate baseline questions:**
  1. Where should someone look for official information during a power outage?
     — evidence: bullets 1 to 3
     — type: resource_seeking
  2. Which devices does the guidance recommend for receiving reports from officials and
     energy suppliers during an outage?
     — evidence: bullet 1
     — type: factual_information
  3. What should someone prepare in advance so they can reach others during an outage?
     — evidence: bullet 3
     — type: procedural_guidance

## 4. Excluded candidates

| Candidate | Reason for exclusion |
|---|---|
| CPSC 468, What to Know About Generators and CO | Overlaps INF-002 in subject matter and adds little: 331 words against 672, covering only the CO hazard where INF-002 also covers electrical and fire hazards and the backfeeding prohibition. It additionally lists the symptoms of CO poisoning and instructs the reader to call 911, which sits close to the medical emergency advice excluded by section 2.3. Retained on disk as evidence of the comparison. |
| FDA, Food and Water Safety During Power Outages and Floods | Derivative of the same federal guidance as INF-003, carrying identical thresholds (4 hours refrigerated, 48 hours full freezer). Selecting both would reproduce the CYB-002/CYB-003 near-duplicate problem. FSIS was preferred as the originating agency. |
| Ready.gov Power Outages HTML page | Fails the stability criterion. Search results show an update date of June 2026, and Ready.gov HTML pages were observed during the DIS batch carrying temporary banners. The frozen PDF equivalent (INF-001) was used instead. |

## 5. Validation

```
$ python scripts/validate_metadata.py corpus/metadata/INF_pilot_sources.csv
=== corpus\metadata\INF_pilot_sources.csv ===
  WARN   row 2: chunk_count is empty (acceptable before Phase 2)
  WARN   row 3: chunk_count is empty (acceptable before Phase 2)
  WARN   row 4: chunk_count is empty (acceptable before Phase 2)
  WARN   row 5: chunk_count is empty (acceptable before Phase 2)
  -> PASSED (4 warning)

$ pytest -q
12 passed in 1.51s
```

The four warnings are empty `chunk_count` values, permitted by the schema before Phase 2.
No tests are skipped: this is the first run since Phase 0 in which all three domain
metadata files contain data. The suite was run six consecutive times with identical
results (12 passed, 1.50-1.53s), which supports the reproducibility requirement.

## 6. Open questions

- **CPSC licence — resolved, no issue raised.** Determined from the CPSC Privacy and
  Security Notice and recorded in the metadata `notes` column.
- **FSIS licence — resolved, no issue raised.** Determined from the FSIS Policies and Links
  page. Note that the USDA non-discrimination statement, which appears prominently on FSIS
  pages, is not a copyright statement and was not used as the basis.
- **DOE licence — resolved, no issue raised.** Determined from the DOE Web Policies page.
- No `needs-review` issues are open for this batch.

## 7. Accepted risks

### 7.1 Two of four sources are HTML captures rather than published files

**Condition.** INF-003 and INF-004 are web pages saved through the browser.

**Impact.** Each checksum is specific to that capture. A later save of either page, after
any template or navigation change, would produce a different checksum even if the article
text were untouched. INF-004 illustrates this directly: the saved file contains a rendered
date of 14 August 2026 that belongs to page furniture rather than to the content.

**Options considered.** (a) accept, recording the capture method and date; (b) search for
PDF equivalents; (c) exclude.

**Decision.** Option (a). Both pages carry explicit dates in their own markup — a footer
line for INF-003 and metadata fields for INF-004 — so the content version is identifiable
independently of the file. Excluding them would mean losing the food safety and official
information channel topics, both named in section 2.1. Capture method and date are recorded
in `notes`.

### 7.2 INF-003 extraction is dominated by site navigation

**Condition.** Raw text extraction of the FSIS page returns approximately 2,655 words, of
which only about 1,782 are the article.

**Evidence.** The remainder is menu content unrelated to the topic: recall summaries by
calendar year, cooking guides, testing programme tables and similar links.

**Impact.** Automated chunking would produce dozens of chunks containing navigation text.
Such chunks would pass the Phase 2 automated checks in section 7.4 — unique chunk_id,
non-empty text, plausible token_count — while being useless as evidence, and they would
distort the corpus by adding food-unrelated vocabulary to the retrieval index.

**Decision.** Navigation must be stripped before chunking. The `document_length` recorded
in the metadata counts the article only, and the discrepancy is documented in `notes` so
that the figure is not mistaken for a raw extraction count.

### 7.3 INF-004 will yield approximately one chunk

**Condition.** The DOE page has 211 words of body content.

**Impact.** All three candidate questions for this document will point to the same evidence
chunk. That is permissible — section 7.1 of the assignment document allows short checklists
to have smaller chunks — but it means INF-004 contributes less scenario diversity than the
other eleven corpus documents.

**Options considered.** (a) accept, and draw fewer baseline questions from this document in
Phase 3; (b) replace it with a longer document on a different topic.

**Decision.** Option (a). It is the only candidate found that addresses official information
channels, one of the four topics named in section 2.1 for this domain, and it is the only
source in the batch from DOE, which is what keeps publisher concentration low.

### 7.4 Medical-adjacent content in two documents

**Condition.** INF-001 refers to the signs of carbon monoxide poisoning, describes them as
flu-like, and advises consulting a doctor about medical devices and refrigerated
medication. The excluded CPSC 468 goes further, listing symptoms and instructing the reader
to call 911.

**Impact.** Section 2.3 excludes diagnosis, treatment and medical emergency advice. Whether
hazard recognition intended to prompt self-evacuation falls under that exclusion is
arguable, but the safer reading is that symptom lists do.

**Decision.** CPSC 468 was excluded partly on this basis. For INF-001, the document is
retained and the affected passages are excluded from ground-truth selection, in the same
way that generator passages in DIS-002 were excluded to avoid cross-domain overlap. Both
exclusions are recorded in `notes`.

### 7.5 Cross-domain overlap with DIS-002: measured and not borne out

Section 7.5 of the DIS screening report flagged a concern that DIS-002, which covers
generator safety and power line hazards, might overlap with the INF batch. That concern was
tested and is not supported: literal 8-gram overlap between DIS-002 and INF-001 is 0.0%,
and between DIS-002 and INF-002 is also 0.0%. Overlap across all pairs in this batch is
0.0%, with the sole exception of INF-003 against INF-004 at 3.6%, which is `.gov` site
boilerplate rather than subject content.

The two CPSC documents were also compared before selection. Exact 8-gram overlap was 0.0%
and 5-gram overlap 0.9%; only three five-word phrases are shared. They are complementary
rather than duplicative, and INF-002 was chosen for being the more substantial of the two.

### 7.6 Taxonomy note carried forward to Phase 3

Across all three domains the twelve corpus documents have produced 33 candidate baseline
questions. The distribution is uneven: `prioritization` appears once, in DIS-003, while
`factual_information` and `procedural_guidance` account for roughly half the total.
Section 8.4 requires that the taxonomy distribution not be badly skewed, so
`prioritization`, `clarification` and `resource_seeking` should be deliberately targeted
when the 30 baseline questions are written in Phase 3.
