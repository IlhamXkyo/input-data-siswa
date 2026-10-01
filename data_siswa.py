import csv
import json
import os
import sys

FILE_DATABASE = "database_siswa.txt"
KKM_KELULUSAN = 75.0


class Siswa:
    def __init__(self, nama="", kelas="", nilai_inggris=0.0, nilai_matematika=0.0, nilai_fisika=0.0):
        self.nama = str(nama).strip()
        self.kelas = str(kelas).strip()
        self.nilai_inggris = float(nilai_inggris)
        self.nilai_matematika = float(nilai_matematika)
        self.nilai_fisika = float(nilai_fisika)

    def hitung_rata_rata(self):
        return (self.nilai_inggris + self.nilai_matematika + self.nilai_fisika) / 3.0

    def predikat(self):
        rata = self.hitung_rata_rata()
        if rata >= 90.0:
            return "A"
        elif rata >= 80.0:
            return "B"
        elif rata >= 70.0:
            return "C"
        elif rata >= 60.0:
            return "D"
        return "E"

    def status_kelulusan(self):
        return "Lulus" if self.hitung_rata_rata() >= KKM_KELULUSAN else "Remedial"

    def ke_string(self):
        nama_bersih = self.nama.replace("|", "/")
        kelas_bersih = self.kelas.replace("|", "/")
        return f"{nama_bersih}|{kelas_bersih}|{self.nilai_inggris:.2f}|{self.nilai_matematika:.2f}|{self.nilai_fisika:.2f}"

    def ke_dict(self):
        return {
            "nama": self.nama,
            "kelas": self.kelas,
            "nilai_inggris": round(self.nilai_inggris, 2),
            "nilai_matematika": round(self.nilai_matematika, 2),
            "nilai_fisika": round(self.nilai_fisika, 2),
            "rata_rata": round(self.hitung_rata_rata(), 2),
            "predikat": self.predikat(),
            "status": self.status_kelulusan()
        }

    @staticmethod
    def dari_string(data_string):
        parts = data_string.strip().split("|")
        if len(parts) == 5:
            try:
                return Siswa(
                    nama=parts[0],
                    kelas=parts[1],
                    nilai_inggris=float(parts[2]),
                    nilai_matematika=float(parts[3]),
                    nilai_fisika=float(parts[4])
                )
            except ValueError:
                return None
        return None


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nTekan Enter untuk melanjutkan...")


def baca_dari_file(filepath=FILE_DATABASE, verbose=True):
    database = []
    if not os.path.exists(filepath):
        if verbose:
            print(f"File database '{filepath}' belum ditemukan. Berkas akan dibuat otomatis.")
        return database

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for baris_ke, line in enumerate(file, start=1):
                clean_line = line.strip()
                if not clean_line:
                    continue
                siswa = Siswa.dari_string(clean_line)
                if siswa:
                    database.append(siswa)
                elif verbose:
                    print(f"Peringatan: Baris ke-{baris_ke} di '{filepath}' dilewati karena format tidak sesuai.")
        if verbose:
            print(f"Memuat {len(database)} data dari file: {filepath}")
    except Exception as error:
        if verbose:
            print(f"Error membaca file database: {error}")
    return database


def simpan_ke_file(database, filepath=FILE_DATABASE):
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            for siswa in database:
                file.write(siswa.ke_string() + "\n")
        return True
    except Exception as error:
        print(f"Gagal menyimpan data ke '{filepath}': {error}")
        return False


def ekspor_ke_csv(database, filepath="rekap_siswa.csv"):
    if not database:
        return False, "Database kosong, tidak ada data untuk diekspor."
    try:
        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "No", "Nama", "Kelas", "B. Inggris", "Matematika", "Fisika", "Rata-rata", "Predikat", "Status"
            ])
            for i, s in enumerate(database, start=1):
                writer.writerow([
                    i, s.nama, s.kelas, f"{s.nilai_inggris:.2f}", f"{s.nilai_matematika:.2f}",
                    f"{s.nilai_fisika:.2f}", f"{s.hitung_rata_rata():.2f}", s.predikat(), s.status_kelulusan()
                ])
        return True, f"Data berhasil diekspor ke format CSV: {filepath}"
    except Exception as error:
        return False, f"Gagal mengekspor CSV: {error}"


def ekspor_ke_json(database, filepath="rekap_siswa.json"):
    if not database:
        return False, "Database kosong, tidak ada data untuk diekspor."
    try:
        data_list = [s.ke_dict() for s in database]
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump({"total_siswa": len(data_list), "data": data_list}, file, indent=2, ensure_ascii=False)
        return True, f"Data berhasil diekspor ke format JSON: {filepath}"
    except Exception as error:
        return False, f"Gagal mengekspor JSON: {error}"


def input_teks_valid(prompt):
    while True:
        teks = input(prompt).strip()
        if not teks:
            print("Input tidak boleh kosong.")
            continue
        return teks.replace("|", "/")


def input_nilai_valid(prompt, nilai_lama=None):
    prompt_str = prompt if nilai_lama is None else f"{prompt} [saat ini: {nilai_lama:.2f}]: "
    while True:
        raw_val = input(prompt_str).strip()
        if nilai_lama is not None and raw_val == "":
            return nilai_lama
        try:
            val = float(raw_val)
            if 0.0 <= val <= 100.0:
                return val
            print("Nilai harus berada dalam rentang 0.0 sampai 100.0.")
        except ValueError:
            print("Input tidak valid. Harap masukkan angka desimal atau bulat.")


def tampilkan_tabel_siswa(daftar_siswa, judul="DATA SISWA"):
    print("=" * 95)
    print(f" {judul.center(93)} ")
    print("=" * 95)
    print(f"{'No':<4} {'Nama':<24} {'Kelas':<10} {'Inggris':<10} {'MTK':<10} {'Fisika':<10} {'Rata-rata':<11} {'Grade':<7} {'Status':<8}")
    print("-" * 95)

    if not daftar_siswa:
        print(" Tidak ada data yang tersedia.".center(95))
    else:
        for i, siswa in enumerate(daftar_siswa, start=1):
            nama_tampil = siswa.nama if len(siswa.nama) <= 22 else siswa.nama[:19] + "..."
            kelas_tampil = siswa.kelas if len(siswa.kelas) <= 8 else siswa.kelas[:7] + "."
            print(
                f"{i:<4} {nama_tampil:<24} {kelas_tampil:<10} "
                f"{siswa.nilai_inggris:<10.2f} {siswa.nilai_matematika:<10.2f} {siswa.nilai_fisika:<10.2f} "
                f"{siswa.hitung_rata_rata():<11.2f} {siswa.predikat():<7} {siswa.status_kelulusan():<8}"
            )
    print("-" * 95)
    print(f"Total: {len(daftar_siswa)} siswa | KKM: {KKM_KELULUSAN:.1f}")
    print("=" * 95)


def input_data_siswa(database):
    while True:
        clear_screen()
        print("=" * 45)
        print("           TAMBAH DATA SISWA BARU")
        print("=" * 45)

        nama = input_teks_valid("Masukkan Nama Lengkap: ")
        kelas = input_teks_valid("Masukkan Kelas (misal 10-A): ")
        nilai_inggris = input_nilai_valid("Masukkan Nilai B. Inggris (0-100): ")
        nilai_matematika = input_nilai_valid("Masukkan Nilai Matematika (0-100): ")
        nilai_fisika = input_nilai_valid("Masukkan Nilai Fisika (0-100): ")

        siswa_baru = Siswa(nama, kelas, nilai_inggris, nilai_matematika, nilai_fisika)
        database.append(siswa_baru)
        simpan_ke_file(database)

        print(f"\nData siswa '{nama}' berhasil disimpan ke database.")
        ulang = input("\nIngin menambah data siswa lain? (y/n): ").strip().lower()
        if ulang != "y":
            break


def tampilkan_data_siswa(database):
    clear_screen()
    if not database:
        print("\nBelum ada data siswa dalam sistem.")
        pause()
        return

    tampilkan_tabel_siswa(database, "REKAPITULASI DATA SISWA")
    pause()


def cari_siswa(database):
    clear_screen()
    if not database:
        print("\nDatabase masih kosong.")
        pause()
        return

    print("=" * 45)
    print("             PENCARIAN SISWA")
    print("=" * 45)
    keyword = input("Masukkan nama atau kelas yang ingin dicari: ").strip().lower()

    if not keyword:
        print("Kata kunci pencarian tidak boleh kosong.")
        pause()
        return

    hasil = [
        s for s in database
        if keyword in s.nama.lower() or keyword in s.kelas.lower()
    ]

    print()
    if hasil:
        tampilkan_tabel_siswa(hasil, f"HASIL PENCARIAN: '{keyword}'")
    else:
        print(f"Tidak ditemukan data siswa dengan kata kunci '{keyword}'.")
    pause()


def edit_data_siswa(database):
    clear_screen()
    if not database:
        print("\nBelum ada data siswa untuk diedit.")
        pause()
        return

    tampilkan_tabel_siswa(database, "PILIH DATA SISWA UNTUK DIEDIT")
    try:
        nomor_str = input("\nMasukkan nomor urut siswa yang ingin diedit (0 untuk batal): ").strip()
        nomor = int(nomor_str)
        if nomor == 0:
            print("Pengeditan dibatalkan.")
            pause()
            return
        if not (1 <= nomor <= len(database)):
            print("Nomor siswa tidak ditemukan.")
            pause()
            return
    except ValueError:
        print("Input nomor tidak valid.")
        pause()
        return

    target = database[nomor - 1]
    print(f"\nMengedit data: {target.nama} ({target.kelas})")
    print("(Tekan Enter langsung jika tidak ingin mengubah data tersebut)")

    nama_baru = input(f"Nama baru [saat ini: {target.nama}]: ").strip()
    if nama_baru:
        target.nama = nama_baru.replace("|", "/")

    kelas_baru = input(f"Kelas baru [saat ini: {target.kelas}]: ").strip()
    if kelas_baru:
        target.kelas = kelas_baru.replace("|", "/")

    target.nilai_inggris = input_nilai_valid("Nilai B. Inggris (0-100)", target.nilai_inggris)
    target.nilai_matematika = input_nilai_valid("Nilai Matematika (0-100)", target.nilai_matematika)
    target.nilai_fisika = input_nilai_valid("Nilai Fisika (0-100)", target.nilai_fisika)

    simpan_ke_file(database)
    print(f"\nData siswa '{target.nama}' berhasil diperbarui dan disimpan.")
    pause()


def hapus_data_siswa(database):
    clear_screen()
    if not database:
        print("\nTidak ada data siswa untuk dihapus.")
        pause()
        return

    tampilkan_tabel_siswa(database, "PILIH DATA SISWA UNTUK DIHAPUS")
    try:
        nomor_str = input("\nMasukkan nomor urut siswa yang akan dihapus (0 untuk batal): ").strip()
        nomor = int(nomor_str)
        if nomor == 0:
            print("Penghapusan dibatalkan.")
            pause()
            return
        if not (1 <= nomor <= len(database)):
            print("Nomor siswa tidak valid.")
            pause()
            return
    except ValueError:
        print("Input tidak valid.")
        pause()
        return

    siswa_terpilih = database[nomor - 1]
    konfirmasi = input(f"Apakah kamu yakin ingin menghapus '{siswa_terpilih.nama}'? (y/n): ").strip().lower()
    if konfirmasi == "y":
        database.pop(nomor - 1)
        simpan_ke_file(database)
        print(f"Data siswa '{siswa_terpilih.nama}' berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")
    pause()


def urutkan_data_siswa(database):
    clear_screen()
    if not database:
        print("\nDatabase masih kosong.")
        pause()
        return

    print("=" * 45)
    print("            URUTKAN DATA SISWA")
    print("=" * 45)
    print("1. Nilai Rata-rata Tertinggi (Peringkat / Ranking)")
    print("2. Nilai Rata-rata Terendah")
    print("3. Abjad Nama (A ke Z)")
    print("4. Abjad Nama (Z ke A)")
    print("5. Berdasarkan Kelas")
    print("0. Batal")
    print("=" * 45)

    pilihan = input("Pilih metode pengurutan (0-5): ").strip()
    if pilihan == "1":
        hasil = sorted(database, key=lambda s: s.hitung_rata_rata(), reverse=True)
        tampilkan_tabel_siswa(hasil, "PERINGKAT NILAI (TERTINGGI KE TERENDAH)")
    elif pilihan == "2":
        hasil = sorted(database, key=lambda s: s.hitung_rata_rata())
        tampilkan_tabel_siswa(hasil, "PERINGKAT NILAI (TERENDAH KE TERTINGGI)")
    elif pilihan == "3":
        hasil = sorted(database, key=lambda s: s.nama.lower())
        tampilkan_tabel_siswa(hasil, "DATA SISWA URUT NAMA (A - Z)")
    elif pilihan == "4":
        hasil = sorted(database, key=lambda s: s.nama.lower(), reverse=True)
        tampilkan_tabel_siswa(hasil, "DATA SISWA URUT NAMA (Z - A)")
    elif pilihan == "5":
        hasil = sorted(database, key=lambda s: (s.kelas.lower(), s.nama.lower()))
        tampilkan_tabel_siswa(hasil, "DATA SISWA URUT BERDASARKAN KELAS")
    elif pilihan == "0":
        return
    else:
        print("Pilihan tidak valid.")
    pause()


def tampilkan_statistik(database):
    clear_screen()
    if not database:
        print("\nBelum ada data siswa untuk dihitung statistiknya.")
        pause()
        return

    total = len(database)
    rata_kelas = sum(s.hitung_rata_rata() for s in database) / total
    rata_inggris = sum(s.nilai_inggris for s in database) / total
    rata_matematika = sum(s.nilai_matematika for s in database) / total
    rata_fisika = sum(s.nilai_fisika for s in database) / total

    siswa_tertinggi = max(database, key=lambda s: s.hitung_rata_rata())
    siswa_terendah = min(database, key=lambda s: s.hitung_rata_rata())

    jumlah_lulus = sum(1 for s in database if s.status_kelulusan() == "Lulus")
    persentase_lulus = (jumlah_lulus / total) * 100.0

    print("=" * 55)
    print("          RINGKASAN & STATISTIK AKADEMIK")
    print("=" * 55)
    print(f"Total Siswa Terdaftar      : {total} siswa")
    print(f"Rata-rata Keseluruhan Kelas : {rata_kelas:.2f}")
    print("-" * 55)
    print(f"Rata-rata B. Inggris       : {rata_inggris:.2f}")
    print(f"Rata-rata Matematika       : {rata_matematika:.2f}")
    print(f"Rata-rata Fisika           : {rata_fisika:.2f}")
    print("-" * 55)
    print(f"Nilai Tertinggi            : {siswa_tertinggi.hitung_rata_rata():.2f} ({siswa_tertinggi.nama} - {siswa_tertinggi.kelas})")
    print(f"Nilai Terendah             : {siswa_terendah.hitung_rata_rata():.2f} ({siswa_terendah.nama} - {siswa_terendah.kelas})")
    print("-" * 55)
    print(f"Kriteria Ketuntasan (KKM)  : {KKM_KELULUSAN:.1f}")
    print(f"Jumlah Siswa Lulus         : {jumlah_lulus} siswa ({persentase_lulus:.1f}%)")
    print(f"Jumlah Siswa Remedial      : {total - jumlah_lulus} siswa ({100.0 - persentase_lulus:.1f}%)")
    print("=" * 55)
    pause()


def menu_ekspor_data(database):
    clear_screen()
    if not database:
        print("\nDatabase kosong, tidak ada data yang bisa diekspor.")
        pause()
        return

    print("=" * 45)
    print("              EKSPOR DATA")
    print("=" * 45)
    print("1. Ekspor ke Berkas CSV (rekap_siswa.csv)")
    print("2. Ekspor ke Berkas JSON (rekap_siswa.json)")
    print("0. Kembali")
    print("=" * 45)

    pilihan = input("Pilih format ekspor (0-2): ").strip()
    if pilihan == "1":
        sukses, pesan = ekspor_ke_csv(database)
        print(f"\n{pesan}")
    elif pilihan == "2":
        sukses, pesan = ekspor_ke_json(database)
        print(f"\n{pesan}")
    elif pilihan == "0":
        return
    else:
        print("Pilihan tidak valid.")
    pause()


def tampilkan_menu_utama():
    print("=" * 46)
    print("       SISTEM REKAPITULASI DATA SISWA")
    print("=" * 46)
    print(" 1. Tambah Data Siswa")
    print(" 2. Lihat Semua Data Siswa")
    print(" 3. Cari Data Siswa (Nama / Kelas)")
    print(" 4. Edit Data Siswa")
    print(" 5. Hapus Data Siswa")
    print(" 6. Urutkan Data (Ranking / Nama / Kelas)")
    print(" 7. Statistik & Analisis Kelas")
    print(" 8. Ekspor Data (CSV / JSON)")
    print(" 0. Keluar dari Program")
    print("=" * 46)


def main():
    database = baca_dari_file(verbose=False)

    while True:
        clear_screen()
        tampilkan_menu_utama()
        pilihan = input("Pilih menu (0-8): ").strip()

        if pilihan == "1":
            input_data_siswa(database)
        elif pilihan == "2":
            tampilkan_data_siswa(database)
        elif pilihan == "3":
            cari_siswa(database)
        elif pilihan == "4":
            edit_data_siswa(database)
        elif pilihan == "5":
            hapus_data_siswa(database)
        elif pilihan == "6":
            urutkan_data_siswa(database)
        elif pilihan == "7":
            tampilkan_statistik(database)
        elif pilihan == "8":
            menu_ekspor_data(database)
        elif pilihan == "0":
            clear_screen()
            print("=" * 46)
            print("Terima kasih. Program selesai dijalankan.")
            print(f"Data tersimpan di berkas: {FILE_DATABASE}")
            print("=" * 46)
            break
        else:
            print("Pilihan tidak dikenali. Silakan pilih menu angka 0 sampai 8.")
            pause()


if __name__ == "__main__":
    main()
