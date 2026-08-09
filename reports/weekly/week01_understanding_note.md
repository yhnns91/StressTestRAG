# Catatan Pemahaman — Minggu 1

*Isi catatan ini setelah membaca dokumen penugasan dan menyelesaikan setup.
Panjang cukup satu halaman. Ini adalah keluaran wajib Fase 0.*

---

## 1. Masalah yang diteliti
Sistem Retrieval-Augmented Generation bekerja dua tahap: mencari potongan
dokumen yang relevan, lalu menyusun jawaban berdasarkan potongan tersebut.
Tahap pencarian bekerja dengan mencocokkan kemiripan bentuk teks, bukan
dengan memahami maksud pertanyaan.

Proyek ini menguji apakah pertanyaan dengan maksud yang sama menghasilkan
kualitas jawaban yang berbeda ketika disampaikan dengan bahasa cemas,
panik, marah, terburu-buru, terfragmentasi, penuh typo, overload, atau
distrustful. Framing ilmiahnya adalah software reliability testing untuk
sistem AI-NLP, bukan diagnosis psikologis.


## 2. Mengapa stressed prompt dapat mengubah retrieval meskipun intent tetap sama
Yang dicocokkan oleh sistem pencarian adalah kemiripan bentuk teks, bukan
maksud di baliknya. Sistem tidak memiliki cara untuk mengetahui bahwa
"whr shld i chk" bermaksud sama dengan "where should I check".

Akibatnya, ketika pertanyaan ditulis dengan banyak typo, singkatan, atau
kalimat terpotong, kemiripannya terhadap dokumen bukti ikut berubah. Potongan
dokumen yang ditemukan bisa meleset, dan kesalahan itu merambat ke tahap
penyusunan jawaban. Dokumen penugasan menyebut kondisi ini sebagai
crisis-induced linguistic noise.


## 3. Pertanyaan pembelajaran Fase 0

**Mengapa full-text sumber tertentu tidak boleh langsung dimasukkan ke repository?**
Dokumen sumber tetap milik penerbitnya, dan hak untuk menyebarkannya ulang
belum tentu kita miliki. Apabila status lisensinya tidak jelas, menyimpan
teks lengkapnya berisiko melanggar hak penerbit.

Yang tetap boleh disimpan adalah metadata, URL, checksum, chunk identifier,
dan script ekstraksi. Keempatnya sudah cukup untuk membuat penelitian dapat
ditelusuri ulang tanpa perlu menyalin isi dokumennya.


**Mengapa direct push ke `main` dilarang?**
Agar setiap perubahan diperiksa lebih dulu sebelum masuk ke versi utama, dan
agar tersedia catatan mengenai siapa mengusulkan apa beserta alasannya. Tanpa
aturan ini, kesalahan dapat langsung mengenai versi utama tanpa terdeteksi
dan tidak ada jejak keputusan yang bisa diaudit.

Saya menguji aturan ini dengan sengaja mencoba mengirim perubahan langsung
ke main. Percobaan pertama berhasil, dan setelah ditelusuri ternyata aturannya
berstatus "not enforced". Setelah konfigurasinya diperbaiki, percobaan
berikutnya ditolak dengan error GH006. Dari situ saya memahami bahwa aturan
yang hanya tertulis berbeda dengan aturan yang ditegakkan sistem.


**Apa perbedaan raw data, interim data, processed data, dan final data?**
Keempatnya menunjukkan tingkat kematangan data. Raw berisi metadata sumber
apa adanya — URL, checksum, dan tanggal akses. Interim adalah data yang masih
dalam proses pengolahan. Processed sudah bersih dan sesuai skema. Final hanya
memuat data yang telah lulus quality control dan layak dirilis.

Pemisahan ini membuat setiap tahap pengolahan dapat ditelusuri, dan mencegah
data yang belum diverifikasi ikut masuk ke rilis.


**Mengapa unit analisis penelitian ini adalah `scenario_id`, bukan sekadar `sample_id`?**
Satu scenario menghasilkan enam sampel yang menanyakan hal yang sama — satu
versi tenang dan lima versi bertekanan. Apabila sebagian masuk ke data latih
dan sebagian ke data uji, sistem sudah pernah melihat pertanyaan itu sebelum
diuji. Kondisi ini disebut leakage, dan membuat hasil pengujian terlihat lebih
baik daripada yang sebenarnya.

Selain itu, analisis statistiknya membandingkan kondisi calm dan stressed secara
berpasangan pada scenario yang sama. Perbandingan itu hanya sah apabila kedua
kondisi berada dalam kelompok yang sama.


## 4. Hal yang masih belum saya pahami
- Cara menghitung dan menafsirkan Fleiss kappa serta Krippendorff alpha pada
  pengukuran agreement antar anotator.
- Cara kerja metrik Faithfulness dan Answer Relevance, khususnya bagaimana
  klaim pada jawaban diverifikasi terhadap evidence.
- Alasan pemilihan uji Wilcoxon signed-rank dibandingkan uji lain untuk
  analisis calm-versus-stressed.


## 5. Referensi
- Dokumen Penugasan StressTestRAG v2.0, 27 Juli 2026
  - Bagian 1.1 — pertanyaan riset
  - Bagian 2.3 — konten yang dilarang
  - Bagian 3.2 — fungsi folder
  - Bagian 3.5 — aturan pull request
  - Bagian 5.3 — pertanyaan pembelajaran
  - Bagian 11.4 — aturan split
  - Bagian 12.3 — analisis statistik