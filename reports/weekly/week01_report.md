# Weekly Report — Week 01

- **Period:** 2026-08-03 to 2026-08-09
- **Phase:** Fase 0 — Persiapan dan Onboarding

---

## Completed

| Issue/PR | Hasil | Angka |
|---|---|---|
| PR #1 | Membersihkan sisa baris uji branch protection dari README | 1 file |
| Issue #3 / PR #4 | Memperbaiki cakupan pemeriksaan secret agar hanya memeriksa file yang dilacak Git | 1 file, 1 test diperbaiki |
| Issue #2 / PR #5 | Menambahkan catatan pemahaman Fase 0 | 5 bagian terisi |
| — | Repository dibuat sesuai struktur Bagian 3.1 | 28 file |
| — | Git LFS dikonfigurasi untuk .jsonl, .parquet, .pdf | 3 pola |
| — | Label dan project board dibuat | 9 label, 6 kolom |

## In Progress

| Issue | Status | Verifikasi |
|---|---|---|
| — | Tidak ada issue aktif | Seluruh issue Fase 0 telah ditutup |

## Quality Metrics

| Metrik | Nilai | Target |
|---|---|---|
| Test result | 9 passed, 3 skipped | pass |
| Dependency terpasang | 33 paket | sesuai requirements.txt |
| Total commit pada main | 8 | — |
| Pull request ter-merge | 3 | — |
| Issue ditutup | 2 | — |
| Direct push ke main | 0 | 0 |
| Keluaran wajib Fase 0 terpenuhi | 4 dari 4 | 4 |

Catatan: 3 test berstatus skipped karena memvalidasi file metadata corpus
yang masih kosong. Ketiganya akan aktif setelah Fase 1 dimulai.

## Blockers

**1. Branch protection tidak ditegakkan pada konfigurasi repository awal**

- **Kondisi:** Aturan larangan direct push ke main tidak berlaku meskipun rule sudah dibuat.
- **Bukti:** Tiga percobaan push langsung ke main berhasil; GitHub menampilkan status "Not enforced" untuk repository private pada free plan.
- **Dampak:** Aturan Bagian 3.5 tidak dapat ditegakkan secara teknis, sehingga kepatuhan hanya bergantung pada disiplin prosedural.
- **Opsi:** (a) mengubah repository menjadi public, (b) memindahkan ke organisasi berbayar, (c) kepatuhan manual.
- **Rekomendasi:** Opsi (a). Sudah diterapkan, dan percobaan berikutnya ditolak dengan error GH006. Mohon konfirmasi apakah konfigurasi public dapat dipertahankan.

**2. False positive pada pemeriksaan secret**

- **Kondisi:** Test test_no_secrets_committed gagal saat verifikasi environment.
- **Bukti:** Dua file cacert.pem milik paket certifi di dalam .venv terdeteksi sebagai pelanggaran, padahal folder tersebut tercantum di .gitignore.
- **Dampak:** CI akan selalu gagal meski tidak ada secret sungguhan, sehingga test kehilangan fungsinya sebagai pengaman.
- **Opsi:** (a) melonggarkan pola pencarian, (b) membatasi pemeriksaan pada file yang dilacak Git.
- **Rekomendasi:** Opsi (b). Sudah diterapkan melalui PR #4; pytest kini lulus tanpa kegagalan.

## Next Week

Target Fase 1 — Reference Corpus dan Metadata, setelah Gate Fase 0 dinyatakan lulus.

- [ ] Kurasi 4 dokumen resmi domain DIS
- [ ] Kurasi 4 dokumen resmi domain INF
- [ ] Kurasi 4 dokumen resmi domain CYB
- [ ] Mengisi metadata 14 kolom untuk 12 dokumen
- [ ] Menyusun laporan screening sumber untuk tiga domain
- [ ] Validasi metadata lulus tanpa error

Issue akan dibuat setelah Gate Fase 0 dikonfirmasi.

## Reference

- Commit: `<isi dengan hasil git log --oneline -1>`
- PR: #1, #4, #5
- Release tag: belum ada