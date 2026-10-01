# Sistem Rekapitulasi Data Siswa (CLI)

Aplikasi Command Line Interface (CLI) berbasis Python murni untuk manajemen akademik siswa. Menyediakan operasi CRUD lengkap, pencarian fleksibel, pengurutan peringkat, analisis statistik kelas, penentuan predikat kelulusan (KKM), serta ekspor data ke format CSV dan JSON.

---

## Fitur Utama

- **Operasi CRUD Lengkap**: Tambah data siswa baru, tampilkan seluruh rekapitulasi, perbarui nilai atau identitas, dan hapus data dengan konfirmasi aman.
- **Pencarian Cepat**: Cari data siswa secara langsung berdasarkan nama atau kelas dengan pencocokan case-insensitive.
- **Peringkat & Pengurutan**: Urutkan data berdasarkan nilai rata-rata (ranking akademik tertinggi ke terendah), urutan abjad nama (A ke Z, Z ke A), atau kelompok kelas.
- **Statistik & Analisis Akademik**: Ringkasan performa kelas meliputi rata-rata keseluruhan, rata-rata tiap mata pelajaran, siswa dengan nilai tertinggi dan terendah, serta persentase kelulusan KKM.
- **Predikat & Status Kelulusan**: Evaluasi nilai otomatis menghasilkan predikat huruf (A, B, C, D, E) dan status akademik (Lulus atau Remedial berdasarkan batas KKM 75.0).
- **Validasi Input Ketat**: Mencegah data kosong, membatasi rentang nilai angka hanya pada 0.0 sampai 100.0, serta sanitasi karakter delimiter berkas teks.
- **Ekspor Data Universal**: Ekspor basis data siswa ke format CSV (`rekap_siswa.csv`) dan JSON (`rekap_siswa.json`) untuk integrasi pelaporan.
- **Penyimpanan Persisten**: Data tersimpan otomatis dalam berkas teks terstruktur dan dimuat kembali setiap aplikasi dijalankan.

---

## Prasyarat

- Python 3.8 atau versi lebih baru (hanya modul standar bawaan Python: `csv`, `json`, `os`, `sys`, `unittest`).

---

## Struktur Menu

```text
 1. Tambah Data Siswa
 2. Lihat Semua Data Siswa
 3. Cari Data Siswa (Nama / Kelas)
 4. Edit Data Siswa
 5. Hapus Data Siswa
 6. Urutkan Data (Ranking / Nama / Kelas)
 7. Statistik & Analisis Kelas
 8. Ekspor Data (CSV / JSON)
 0. Keluar dari Program
```

---

## Cara Menjalankan

1. Kloning repositori:
   ```bash
   git clone https://github.com/IlhamXkyo/input-data-siswa.git
   cd input-data-siswa
   ```

2. Jalankan aplikasi:
   ```bash
   python data_siswa.py
   ```

3. Jalankan pengujian unit (unit tests):
   ```bash
   python -m unittest test_data_siswa.py -v
   ```

---

## Format Data Penyimpanan

Setiap entri siswa disimpan per baris dalam berkas `database_siswa.txt` dengan format:

```text
Nama Siswa|Kelas|Nilai Inggris|Nilai Matematika|Nilai Fisika
```

Contoh:
```text
Ahmad Fauzi|10-A|85.00|90.00|88.00
Citra Lestari|10-B|92.00|95.00|94.00
```

---

## Lisensi

Didistribusikan di bawah Lisensi MIT. Silakan lihat berkas [LICENSE](LICENSE) untuk informasi lebih lanjut.
