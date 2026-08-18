# Source Screening — DIS

- **Issue:** #10
- **Branch:** `task/issue-010-disaster-corpus-metadata`
- **Commit:** `00d9587`
- **Date:** 2026-08-18

---

> Page references in this section use PDF viewer page numbers.

## 1. Search strategy

**Publishers consulted.** Screening was restricted to national emergency management
agencies and national meteorological services, on the grounds that their publications are
stable, authored under a clear institutional mandate, and issued in English. Two were
searched directly: the Federal Emergency Management Agency through its Ready Campaign
(ready.gov), and NOAA's National Weather Service (weather.gov). UNDRR and IFRC were held
in reserve in case fewer than four documents met the criteria; they were not needed.

**Search terms used.**
- ready.gov emergency supply kit checklist PDF
- National Weather Service watch warning advisory difference
- ready.gov evacuation plan before during after
- ready.gov earthquake safety drop cover hold on
- "Family Emergency Communication Plan" ready.gov PDF

Searching was carried out with assistant support; the terms above are the ones that
produced the accepted candidates.

**Lesson applied from the CYB batch.** Document length was checked before download rather
than after. In the CYB batch three of four accepted documents exceeded the 2-10 page
screening range and required scope limitations to be written into the report. All four DIS
candidates fall inside the range.

**Sources deliberately not used.** Blogs, vendor material, discussion forums and news
articles were excluded on principle rather than case by case. Section 6.7 of the assignment
document identifies reliance on such sources as a common failure, and none satisfies the
requirement for an identifiable publishing authority or for content stability over time.

**Ready.gov HTML pages were also rejected as a class.** Search results showed the
evacuation, kit and planning pages carrying update dates of March, April, June and July
2026, and one page was displaying a temporary banner about a lapse in federal funding.
Pages that change this often cannot be checksummed meaningfully. The frozen PDF
publications were used instead.

## 2. Candidates evaluated

| # | Publisher | Title | URL | Decision |
|---|---|---|---|---|
| 1 | FEMA | Be Prepared for an Earthquake (V-1003) | https://www.ready.gov/sites/default/files/2024-03/ready.gov_earthquake_hazard-info-sheet.pdf | include |
| 2 | FEMA | Be Prepared for a Flood (V-1005) | https://www.ready.gov/sites/default/files/2024-03/ready.gov_flood_hazard-info-sheet.pdf | include |
| 3 | FEMA | Be Prepared for a Tornado (V-1010) | https://www.ready.gov/sites/default/files/2024-08/ready-gov_tornado_info-sheet.pdf | include |
| 4 | NWS / NOAA | Flood Warning VS. Watch | https://www.weather.gov/safety/flood-watch-warning | include |
| 5 | FEMA | Emergency Supply List | ready.gov | exclude |
| 6 | FEMA | Family Emergency Communication Plan (P-1094) | ready.gov | exclude |
| 7 | FEMA / Ready | Evacuation | https://www.ready.gov/evacuation | exclude |

## 3. Included documents

### DIS-001 — Be Prepared for an Earthquake (FEMA V-1003)

- **Publisher:** Federal Emergency Management Agency, U.S. Department of Homeland
  Security — ready.gov
- **Why authoritative:** FEMA is the US federal emergency management agency. The sheet
  carries the FEMA seal and an official publication number, and is distributed through the
  agency's Ready Campaign site.
- **Why stable:** A standing preparedness sheet, not a live alert. The publisher states on
  ready.gov/publications that these publications are current as of 30 September 2025 and
  will not be updated on a regular basis after that date, which is an explicit stability
  guarantee of a kind the CYB batch did not have.
- **Structure:** 2 pages, approximately 525 words. Page 1 is a cover panel with a hazard
  definition, four characteristic icons, and immediate protective actions. Page 2 carries
  three clearly headed sections — Prepare NOW, Survive DURING, Be Safe AFTER — followed by
  a short closing block. The three headings give clean semantic chunk boundaries.
- **License status:** `open_license_redistributable`. No licence statement appears inside
  the PDF. The status was determined from the Reprint Terms of Use at ready.gov/publications,
  which permit reproduction on two conditions: that content, photos, graphics and figures
  are not altered in any way, and that the material is not used so as to imply FEMA or US
  Government endorsement. `public_domain` was not used because the schema defines it as
  carrying no copyright restriction, and conditions do apply here.
- **Safety level:** `medium`. The schema defines `medium` as containing procedural detail
  that must be quoted carefully. The sheet gives specific protective procedures and specific
  prohibitions, and unlike the CYB material an incorrectly grounded answer here bears on
  physical safety rather than on a regulatory duty.
- **Candidate baseline questions:**
  1. What are the three actions that make up Drop, Cover, and Hold On?
     — evidence: p.2, "Prepare NOW"
     — type: factual_information
  2. Is a doorway a recommended place to shelter during an earthquake?
     — evidence: p.1, cover panel protective actions
     — type: misinformation_correction
  3. What should someone do if an earthquake happens while they are in a vehicle?
     — evidence: p.2, "Survive DURING"
     — type: procedural_guidance

### DIS-002 — Be Prepared for a Flood (FEMA V-1005)

- **Publisher:** Federal Emergency Management Agency, U.S. Department of Homeland
  Security — ready.gov
- **Why authoritative:** As DIS-001. FEMA seal and publication number V-1005.
- **Why stable:** As DIS-001; covered by the same 30 September 2025 freeze statement.
- **Structure:** 2 pages, approximately 696 words, following the same cover-plus-three-sections
  layout as DIS-001. See section 7.1 for a text-layer defect affecting extraction.
- **License status:** `open_license_redistributable`, on the same basis as DIS-001.
- **Safety level:** `medium`. The sheet carries specific numeric thresholds for when moving
  water becomes dangerous to a person and to a vehicle. A misquoted figure in this context
  is directly hazardous.
- **Candidate baseline questions:**
  1. What should someone do if they become trapped in a building during a flood?
     — evidence: p.2, "Survive DURING"
     — type: procedural_guidance
  2. Where can someone find information about the type of flood risk in their area?
     — evidence: p.2, "Prepare NOW"
     — type: resource_seeking
  3. Does a standard homeowner's insurance policy cover flooding?
     — evidence: p.2, "Prepare NOW"
     — type: misinformation_correction

### DIS-003 — Be Prepared for a Tornado (FEMA V-1010)

- **Publisher:** Federal Emergency Management Agency, U.S. Department of Homeland
  Security — ready.gov
- **Why authoritative:** As DIS-001. FEMA seal and publication number V-1010.
- **Why stable:** As DIS-001; covered by the same 30 September 2025 freeze statement.
- **Structure:** 2 pages, approximately 535 words, same layout as DIS-001 and DIS-002. The
  cover panel presents shelter options in descending order of preference, which supports a
  prioritization-type question — the one taxonomy category not represented in the CYB batch.
- **License status:** `open_license_redistributable`, on the same basis as DIS-001.
- **Safety level:** `medium`. The sheet gives specific shelter instructions and a specific
  prohibition against sheltering under an overpass or bridge.
- **Candidate baseline questions:**
  1. Which shelter locations should be prioritized when a tornado warning is issued?
     — evidence: p.1, cover panel
     — type: prioritization
  2. What signs may indicate that a tornado is approaching?
     — evidence: p.2, "Prepare NOW"
     — type: factual_information
  3. How does the guide recommend communicating with family and friends after a tornado?
     — evidence: p.2, "Be Safe AFTER"
     — type: procedural_guidance

### DIS-004 — Flood Warning VS. Watch

- **Publisher:** NOAA's National Weather Service, U.S. Department of Commerce — weather.gov
- **Why authoritative:** The NWS is the US national meteorological service and the body that
  issues these alert products. The page metadata names NOAA's National Weather Service as
  publisher and the US Department of Commerce as creator.
- **Why stable:** A definitional reference page, not an active alert. Page metadata records
  a creation date of 26 February 2024. The page explains what the alert levels mean rather
  than announcing any current condition.
- **Structure:** One page, approximately 392 words. Four bolded definitions — Flash Flood
  Warning, Flood Warning, Flood Advisory, Flood Watch — each self-contained. Saved locally
  as HTML; see section 7.4.
- **License status:** `public_domain`. weather.gov/disclaimer states that NWS web page
  information is in the public domain unless specifically annotated otherwise and may be
  used without charge for any lawful purpose. An attribution requirement accompanies it:
  third parties producing copyrighted works consisting predominantly of NWS material must
  identify that material and state that it is not subject to copyright protection. This is
  to be reflected in the dataset card at Phase 8.
- **Safety level:** `low`. The page defines what each alert level means without instructing
  the reader to take any specific physical action.
- **Candidate baseline questions:**
  1. What is the difference between a Flood Watch and a Flood Warning?
     — evidence: definitions of Flood Warning and Flood Watch
     — type: clarification
  2. When is a Flood Advisory issued?
     — evidence: Flood Advisory definition
     — type: factual_information
  3. What action does the National Weather Service advise when a Flash Flood Warning is
     issued?
     — evidence: Flash Flood Warning definition
     — type: factual_information

## 4. Excluded candidates

| Candidate | Reason for exclusion |
|---|---|
| FEMA Emergency Supply List | Content is a checklist of items rather than prose; would support one or two questions at most, not the three required by the screening criteria. Four differing versions of the same list are in circulation on ready.gov, making version identification unreliable. |
| FEMA Family Emergency Communication Plan (P-1094) | Substantially a fill-in form with blank contact cards. This is the same defect that limited CYB-002 and CYB-003: an instruction to the reader to supply their own content cannot serve as evidence. |
| Ready.gov Evacuation page | Fails the stability criterion. Search results show the page updated in March 2026, and related Ready.gov pages were displaying a temporary banner about a lapse in federal funding. A checksum taken today would not be reproducible. |

## 5. Validation

```
$ python scripts/validate_metadata.py corpus/metadata/DIS_pilot_sources.csv
=== corpus\metadata\DIS_pilot_sources.csv ===
  WARN   row 2: chunk_count is empty (acceptable before Phase 2)
  WARN   row 3: chunk_count is empty (acceptable before Phase 2)
  WARN   row 4: chunk_count is empty (acceptable before Phase 2)
  WARN   row 5: chunk_count is empty (acceptable before Phase 2)
  -> PASSED (4 warning)

$ pytest -q
11 passed, 1 skipped in 1.13s
```

The four warnings are empty `chunk_count` values, which the schema permits before Phase 2.
The single skipped test is `INF_pilot_sources.csv`, which has no data rows yet; the skip
count fell from two to one when this batch was added.

## 6. Open questions

- **FEMA licence conditions — resolved, no issue raised.** No licence statement appears
  inside the three PDFs. The Reprint Terms of Use at ready.gov/publications were consulted
  and recorded in the metadata `notes` column. One condition — that content must not be
  altered — is noted in section 7.2 as requiring attention at Phase 2.
- **NWS licence — resolved, no issue raised.** weather.gov/disclaimer confirms public domain
  status with an attribution requirement, recorded in `notes`.
- No `needs-review` issues are open for this batch.

## 7. Accepted risks

Four issues were identified. None led to a document being rejected, so each is recorded
here with the reasoning and the handling planned for Phase 2.

### 7.1 DIS-002 contains two overlapping text layers

**Condition.** The flood sheet stores two versions of its display text on top of one another.

**Evidence.** Automated text extraction returns interleaved fragments — for example
"ARE / BE YOU READY / PREPARED FORFOR / A A / FLOOD? / FLOOD". An earlier edition titled
"ARE YOU READY FOR A FLOOD?" remains beneath the current "BE PREPARED FOR A FLOOD". Only
the current version is visible on screen. DIS-001 and DIS-003 do not show this defect.

**Impact.** Chunks produced by automated extraction from the affected regions would contain
unreadable mixed text. Such a chunk would pass the Phase 2 automated checks in section 7.4
of the assignment document — the chunk_id would be unique, the text non-empty, the
token_count plausible — while being useless as evidence. The reported `document_length` of
696 words is also inflated by the duplicated layer.

**Options considered.** (a) clean the affected regions manually during Phase 2; (b) extract
with a different tool or setting and compare; (c) exclude the document.

**Decision.** Options (a) and (b) together. The defect is confined to the cover panel, so
the three-section prose on page 2 — from which all three candidate questions are drawn — is
unaffected. The condition is recorded in the metadata `notes` column so that it is not
rediscovered as a surprise during chunking.

### 7.2 FEMA reprint terms restrict alteration

**Condition.** The Reprint Terms of Use require that content, photos, graphics and figures
not be altered in any way. Phase 2 requires the documents to be divided into chunks.

**Evidence.** ready.gov/publications, Reprint Terms of Use.

**Impact.** Whether chunking constitutes alteration is genuinely open. Chunking preserves
the wording exactly and each chunk retains its document_id and source_url, which argues
that it does not; distributing fragments of a document is nevertheless not distributing the
document in its original form.

**Options considered.** (a) record `open_license_redistributable` and preserve wording
exactly, with full source attribution on every chunk; (b) record `metadata_only_until_verified`
and store no text; (c) exclude the FEMA documents.

**Decision.** Option (a). Chunk text will be copied verbatim with no editorial correction,
and each chunk will retain document_id, heading and source_url so that any excerpt can be
traced to the unaltered original. `public_domain` was deliberately not used, since the
schema reserves that value for material carrying no restriction at all.

### 7.3 DIS-003 contains a typographical error in the source text

**Condition.** The tornado sheet reads "Do not get under an overpas or bridge", missing a
letter.

**Impact.** If that passage becomes an evidence chunk, `ground_truth_context` must reproduce
the error verbatim. Silently correcting it would break traceability between the chunk and
the source document, and under 7.2 would also constitute alteration.

**Decision.** Reproduce verbatim; recorded in the metadata `notes` column. The candidate
questions selected for DIS-003 avoid this passage, so the situation is unlikely to arise.

### 7.4 DIS-004 is an HTML capture rather than a published file

**Condition.** The NWS source is a web page, saved locally through the browser rather than
downloaded as a file.

**Impact.** The checksum is specific to that capture. A later save of the same page — after
any template, navigation or footer change — would produce a different checksum even if the
four definitions were untouched. This weakens reproducibility relative to the three PDFs.

**Options considered.** (a) accept, recording the capture method and date; (b) search for a
PDF equivalent from NWS; (c) exclude.

**Decision.** Option (a). The page carries an explicit creation date in its metadata, its
content is definitional rather than time-sensitive, and it is the only candidate from a
publisher other than FEMA — which is what keeps cross-document overlap in this domain near
zero. The capture method and date are recorded in `notes`.

### 7.5 Note on cross-domain and cross-document overlap

Literal 8-gram overlap between the four accepted documents was measured and is negligible:
0.2% between DIS-001 and DIS-003, 0.9% between DIS-002 and DIS-003, 0.2% between DIS-001
and DIS-002, and 0.0% between DIS-004 and each of the others. For comparison, the same
measure between CYB-002 and CYB-003 was 23%. No near-duplicate handling is required for
this domain.

Two smaller points were nevertheless allowed for when selecting candidate questions. First,
DIS-002 covers generator safety and power line hazards, which are INF domain topics under
section 2.1; ground-truth chunks from those passages are avoided to prevent cross-domain
overlap once the INF batch is curated. Second, DIS-001 and DIS-003 give similar advice on
signalling for help when trapped and on protective clothing during clean-up; questions were
drawn from other sections so that no baseline question could be answered from both sheets.
