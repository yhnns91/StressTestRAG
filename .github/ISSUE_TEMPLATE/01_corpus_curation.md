---
name: Corpus curation
about: Kurasi dokumen sumber resmi untuk satu domain
title: "[Corpus] Curate N official <domain> documents for pilot corpus"
labels: corpus
---

## Objective
Apa yang harus dicapai dan mengapa penting.

## Scope
**Termasuk:**
-

**Tidak termasuk:**
-

## Deliverables
- `corpus/metadata/<DOMAIN>_pilot_sources.csv`
- `reports/qc/<DOMAIN>_source_screening.md`

## Acceptance Criteria
- [ ] Sumber berasal dari lembaga resmi atau organisasi otoritatif
- [ ] Dokumen stabil, bukan live alert atau berita
- [ ] Bahasa Inggris dengan struktur heading/paragraf jelas
- [ ] Konten berupa guidance umum yang aman dan non-eksploitatif
- [ ] `license_status` terisi
- [ ] URL aktif, `download_date` dan `checksum` tersimpan
- [ ] Alasan eksklusi dicatat untuk kandidat yang ditolak
- [ ] `python scripts/validate_metadata.py <file>` lulus

## References
-
