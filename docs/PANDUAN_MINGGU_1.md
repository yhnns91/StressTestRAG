# Panduan Eksekusi Minggu 1

Dokumen ini berisi urutan langkah konkret untuk menyelesaikan Fase 0 dan Fase 1.
Hapus file ini sebelum rilis publik — ini catatan kerja internal, bukan bagian dari dataset.

---

## Hari 1 — Repository online

### 1.1 Buat repository di GitHub

Buka github.com → **New repository**:

- Nama: `StressTestRAG`
- Visibility: **Private** dulu (bisa diubah ke public sebelum rilis)
- **Jangan** centang "Add a README file" — kerangka ini sudah punya

### 1.2 Push kerangka ini

```bash
cd StressTestRAG

git init
git branch -M main
git add .
git commit -m "chore(repo): initialize repository structure and tooling"
git remote add origin https://github.com/<username>/StressTestRAG.git
git push -u origin main
```

### 1.3 Aktifkan Git LFS

```bash
git lfs install
```

File `.gitattributes` sudah mengatur pelacakan `*.jsonl`, `*.parquet`, dan `*.pdf`.

### 1.4 Lindungi branch `main`

Di GitHub: **Settings → Branches → Add branch protection rule**

- Branch name pattern: `main`
- ✅ Require a pull request before merging
- ✅ Require status checks to pass before merging

Ini yang membuat aturan "tidak ada direct push ke main" berlaku secara teknis, bukan sekadar niat baik.

### 1.5 Buat label

**Issues → Labels → New label**, buat sembilan label berikut:

`corpus` · `baseline` · `stress-variant` · `annotation` · `qc` · `experiment` · `documentation` · `blocked` · `needs-review`

### 1.6 Buat GitHub Project

**Projects → New project → Board**, dengan kolom:

`Backlog` · `Ready` · `In Progress` · `In Review` · `Needs Revision` · `Done`

---

## Hari 2 — Environment dan latihan alur kerja

### 2.1 Virtual environment

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
pytest -q
```

Semua test harus lulus. Kalau `test_repo_structure.py` gagal, ada folder atau file yang hilang.

### 2.2 Latihan siklus GitHub

Ini keluaran wajib Fase 0: satu PR onboarding kecil. Lakukan **prosedur lengkap**, jangan potong kompas.

```bash
# 1. Buat Issue di web GitHub, catat nomornya (misal #1)
#    Judul: "[Docs] Add supervisor and project period to README"

# 2. Buat branch
git checkout -b docs/issue-001-readme-project-info

# 3. Edit README.md — tambahkan nama pembimbing dan periode proyek

# 4. Commit
git add README.md
git commit -m "docs(readme): add supervisor and project period"

# 5. Push
git push -u origin docs/issue-001-readme-project-info

# 6. Buka Pull Request di web, isi template, tulis "Closes #1"

# 7. Merge, lalu bersihkan
git checkout main
git pull
git branch -d docs/issue-001-readme-project-info
```

Ulangi minimal tiga kali dengan perubahan kecil lain sampai tanganmu hafal.

### 2.3 Isi catatan pemahaman

Buka `reports/weekly/week01_understanding_note.md` dan isi seluruh bagiannya. Empat pertanyaan pembelajaran di dalamnya berasal langsung dari Bagian 5.3 dokumen penugasan.

---

## Hari 3–5 — Kurasi 12 dokumen

### 3.1 Buat tiga Issue

Satu per domain, pakai template **Corpus curation**:

- `[Corpus] Curate four official disaster preparedness documents for pilot corpus`
- `[Corpus] Curate four official power outage documents for pilot corpus`
- `[Corpus] Curate four official cyber incident reporting documents for pilot corpus`

### 3.2 Alur kerja per dokumen

Untuk setiap kandidat:

1. **Cari** dari lembaga resmi. Hindari blog, forum, dan berita.
2. **Baca utuh** — bukan hanya cuplikan hasil pencarian. Ini yang paling sering dilewati.
3. **Nilai** dengan checklist inklusi (lihat di bawah).
4. **Unduh** file-nya ke folder sementara di luar repo.
5. **Hitung checksum:**
   ```bash
   python scripts/compute_checksum.py ~/downloads/nama-file.pdf
   ```
6. **Catat** ke `corpus/metadata/<DOMAIN>_pilot_sources.csv`.
7. **Tulis alasan** inklusi atau eksklusi di laporan screening.

### 3.3 Checklist inklusi

- [ ] Sumber dari lembaga resmi atau organisasi otoritatif
- [ ] Dokumen stabil — bukan live alert atau berita yang berubah cepat
- [ ] Bahasa Inggris dengan struktur heading dan paragraf jelas
- [ ] Konten berupa guidance umum yang aman dan non-eksploitatif
- [ ] Status lisensi dicatat
- [ ] URL dan tanggal akses tersimpan
- [ ] Cakupan cukup fokus — satu pertanyaan tidak menuntut banyak interpretasi

### 3.4 Aturan lisensi

Kalau ragu, isi `license_status` dengan `metadata_only_until_verified`, dan **jangan simpan full-text**. Cukup metadata, URL, checksum, dan script ekstraksi.

Ini bukan kompromi — dokumen penugasan secara eksplisit mengizinkannya, dan tetap sah secara ilmiah.

### 3.5 Validasi

```bash
python scripts/validate_metadata.py corpus/metadata/DIS_pilot_sources.csv
python scripts/validate_metadata.py corpus/metadata/INF_pilot_sources.csv
python scripts/validate_metadata.py corpus/metadata/CYB_pilot_sources.csv
```

Perbaiki semua `ERROR`. Baca setiap `WARN` dan pastikan kamu paham kenapa muncul.

### 3.6 Tulis laporan screening

Salin `reports/qc/TEMPLATE_source_screening.md` menjadi `reports/qc/<DOMAIN>_source_screening.md` untuk tiap domain, lalu isi.

Bagian **"Excluded candidates"** sering diabaikan padahal penting — kemampuan menjelaskan mengapa sebuah dokumen ditolak adalah bagian dari kriteria kelulusan Gate Fase 1.

### 3.7 Buka Pull Request

Satu PR per domain, maksimal 4–6 dokumen agar review terfokus. Lampirkan output validasi dan 3–5 contoh row.

---

## Akhir minggu — Gate Fase 1

Ajukan ke pembimbing bila semua terpenuhi:

- [ ] 12 dokumen memiliki metadata lengkap dan tervalidasi
- [ ] Keputusan inklusi dan eksklusi dapat dijelaskan
- [ ] Tidak ada sumber berisiko tinggi tanpa review
- [ ] Laporan screening tersedia untuk tiga domain
- [ ] Catatan pemahaman terisi
- [ ] PR onboarding sudah ter-merge
- [ ] Laporan mingguan terisi di `reports/weekly/`

---

## Kesalahan umum yang harus dihindari

| Kesalahan | Kenapa bermasalah |
|---|---|
| Memakai blog atau berita karena lebih mudah dibaca | Bukan sumber otoritatif; melanggar kriteria inklusi |
| Tidak mencatat lisensi dan tanggal akses | Dataset tidak dapat diaudit; menghambat rilis |
| Menyimpan PDF penuh tanpa memastikan hak redistribusi | Risiko hukum; melanggar Bagian 2.3 |
| Memilih dokumen yang terlalu luas | Satu pertanyaan jadi butuh banyak interpretasi; answerability sulit dijamin |
| Langsung membuat prompt stres | Data tanpa sumber; harus dibuang |
| Push langsung ke `main` | Tidak ada audit trail; melanggar Bagian 3.5 |

---

## Yang belum boleh dikerjakan

Minggu ini berhenti di metadata. **Jangan** melakukan chunking, menulis baseline question, atau membuat stress variant sebelum Gate Fase 1 dinyatakan lulus oleh pembimbing.
