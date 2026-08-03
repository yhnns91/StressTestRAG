# Panduan Kontribusi

Dokumen ini adalah panduan kerja internal. Bahasa Indonesia dipakai di sini agar mudah diikuti; seluruh **data** (corpus, question, prompt, ground-truth answer) tetap berbahasa Inggris.

---

## 1. Prinsip dasar

GitHub adalah sumber kebenaran tunggal. File di komputer lokal hanya area kerja sementara. Versi yang diakui adalah versi yang sudah masuk repository melalui pull request.

**Urutan kerja terkunci:**

```
corpus resmi → chunk → evidence chunk → baseline question
→ stress variants → anotasi → QC → pilot RAG → rilis
```

Satu fase tidak boleh dimulai sebelum gate fase sebelumnya dinyatakan lulus.

---

## 2. Siklus kerja satu unit tugas

```
Issue → branch → commit → push → pull request → review → merge
```

Langkah demi langkah:

1. Buat GitHub Issue untuk satu unit tugas, pakai template yang tersedia.
2. Assign issue tersebut dan tambahkan label yang sesuai.
3. Buat branch dari `main`.
4. Kerjakan, lalu commit dalam potongan kecil secara berkala.
5. Push branch ke remote.
6. Buka pull request yang menghubungkan issue (`Closes #NN`).
7. Jalankan checklist PR dan tunggu review.
8. Perbaiki seluruh komentar review.
9. Merge setelah disetujui dan CI lulus.

---

## 3. Konvensi penamaan

### Branch

```
task/issue-012-disaster-corpus-metadata
task/issue-021-baseline-power-outage
fix/issue-037-remove-near-duplicates
docs/issue-044-annotation-guideline
```

Format: `<tipe>/issue-<nomor>-<deskripsi-singkat>`
Tipe yang dipakai: `task`, `fix`, `docs`, `test`, `chore`.

### Commit

```
feat(corpus): add 12 official source records
data(baseline): add 10 disaster QA pairs
data(stress): add anxious and fragmented variants for DIS batch 01
fix(qc): remove duplicated scenario identifiers
docs(guideline): clarify semantic equivalence score 4
test(split): verify no scenario-level leakage
chore(repo): configure Git LFS tracking
```

Format: `<tipe>(<scope>): <deskripsi hasil>`
Tulis **hasil**, bukan aktivitas. Bandingkan "add 12 official source records" dengan "update file".

### ID objek data

| Objek | Format | Contoh |
|---|---|---|
| Document | `[DOMAIN]-[3 digit]` | `DIS-001`, `INF-014`, `CYB-009` |
| Chunk | `[document_id]_C[2 digit]` | `DIS-001_C03` |
| Scenario | `[DOMAIN]-S[3 digit]` | `INF-S012` |
| Sample | `STR-[6 digit]` | `STR-000184` |
| Annotation batch | `ANN-[YYYYMMDD]-B[2 digit]` | `ANN-20260805-B01` |

---

## 4. Aturan pull request

- [ ] PR hanya membahas satu issue atau satu unit kerja yang jelas.
- [ ] Judul menjelaskan hasil, bukan aktivitas umum.
- [ ] Deskripsi memuat tujuan, file yang berubah, cara memeriksa, hasil QC, dan risiko tersisa.
- [ ] Untuk perubahan data, lampirkan 3–5 contoh row.
- [ ] Cantumkan `Closes #NN`.
- [ ] Tidak ada direct push ke `main`.
- [ ] Semua komentar review diselesaikan sebelum merge.

Batasi satu PR corpus pada 4–6 dokumen agar review tetap terfokus.

---

## 5. Label yang dipakai

`corpus` · `baseline` · `stress-variant` · `annotation` · `qc` · `experiment` · `documentation` · `blocked` · `needs-review`

### Kapan memakai `needs-review`

Hentikan item dan buat issue berlabel `needs-review` apabila:

- Lisensi atau hak penyimpanan full-text tidak jelas.
- Prompt tampak menambah fakta atau mengubah intent.
- Evidence chunk tidak cukup menjawab baseline question.
- Anotator berulang kali tidak sepakat pada label yang sama.
- Ditemukan konten medical, self-harm, exploitative cyber, atau dangerous detail.
- QC menghasilkan near-duplicate atau leakage yang tidak dapat diselesaikan otomatis.

---

## 6. Aturan penyimpanan file

| Folder | Boleh berisi | Larangan |
|---|---|---|
| `data/raw_external_metadata/` | Metadata sumber, URL, checksum, tanggal akses | Full-text berlisensi tidak jelas |
| `corpus/extracted_text/` | Teks hasil ekstraksi yang legal disimpan | Mengedit file sumber manual tanpa log |
| `corpus/chunks/` | Chunk terstruktur dengan ID dan source trace | Chunk tanpa `document_id` |
| `annotations/` | Guideline, batch anotasi, hasil adjudication | Menimpa batch lama |
| `data/final/` | Dataset release candidate dan final | Apa pun yang belum lulus QC |
| `scripts/`, `src/`, `tests/` | Pipeline dan pengujian reproducibility | Notebook sebagai satu-satunya implementasi |
| `reports/` | QC, agreement, statistik, laporan mingguan | Laporan tanpa referensi commit |

**Jangan pernah commit:** credential, API key, secret, data pribadi, cache model, virtual environment, atau hasil build.

---

## 7. Standar komunikasi masalah

Setiap masalah disampaikan dengan urutan:

```
kondisi yang ditemukan → bukti → dampak → opsi solusi → rekomendasi
```

Hindari laporan yang hanya menyebut data "error" atau "tidak bisa" tanpa angka dan bukti.

**Contoh:**

> **Kondisi:** Enam chunk pada INF-003 memiliki `token_count` di bawah rentang target.
> **Bukti:** Output `validate_chunks.py` pada commit `a1b2c3d`, baris 12–17.
> **Dampak:** Chunk terlalu pendek berisiko kehilangan konteks sehingga evidence tidak berdiri sendiri.
> **Opsi:** (a) gabungkan dengan paragraf berikutnya, (b) tandai sebagai pengecualian karena berupa checklist.
> **Rekomendasi:** Opsi (b), karena keenam chunk berasal dari bagian checklist yang memang ringkas.

---

## 8. Setup environment

```bash
git clone <repository-url>
cd StressTestRAG

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
pytest -q
```

Git LFS hanya perlu dikonfigurasi sekali:

```bash
git lfs install
```

File `.gitattributes` sudah mengatur pelacakan untuk `*.jsonl`, `*.parquet`, dan `*.pdf`.
