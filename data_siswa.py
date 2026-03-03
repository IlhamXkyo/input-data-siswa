import os
import sys

# Nama file database
FILE_DATABASE = "database_siswa.txt"

# Class untuk menyimpan data siswa
class Siswa:
    def __init__(self, nama="", kelas="", nilai_inggris=0, nilai_matematika=0, nilai_fisika=0):
        self.nama = nama
        self.kelas = kelas
        self.nilai_inggris = float(nilai_inggris)
        self.nilai_matematika = float(nilai_matematika)
        self.nilai_fisika = float(nilai_fisika)
    
    def hitung_rata_rata(self):
        return (self.nilai_inggris + self.nilai_matematika + self.nilai_fisika) / 3.0
    
    def ke_string(self):
        # Konversi ke format untuk disimpan di file
        return f"{self.nama}|{self.kelas}|{self.nilai_inggris}|{self.nilai_matematika}|{self.nilai_fisika}"
    
    @staticmethod
    def dari_string(data_string):
        # Membuat objek Siswa dari string
        parts = data_string.strip().split('|')
        if len(parts) == 5:
            return Siswa(
                nama=parts[0],
                kelas=parts[1],
                nilai_inggris=float(parts[2]),
                nilai_matematika=float(parts[3]),
                nilai_fisika=float(parts[4])
            )
        return None

def clear_screen():
    """Bersihkan layar terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    """Jeda program sampai user tekan Enter"""
    input("\nTekan Enter untuk melanjutkan...")

def baca_dari_file():
    """Baca data siswa dari file"""
    database = []
    try:
        with open(FILE_DATABASE, 'r') as file:
            for line in file:
                siswa = Siswa.dari_string(line)
                if siswa:
                    database.append(siswa)
        print(f"Memuat {len(database)} data dari file...")
    except FileNotFoundError:
        print("File database belum ada. Akan dibuat saat pertama kali menyimpan.")
    except Exception as e:
        print(f"Error membaca file: {e}")
    
    pause()
    return database

def simpan_ke_file(database):
    """Simpan data siswa ke file"""
    try:
        with open(FILE_DATABASE, 'w') as file:
            for siswa in database:
                file.write(siswa.ke_string() + '\n')
        print(f"Data berhasil disimpan ke file: {FILE_DATABASE}")
    except Exception as e:
        print(f"Gagal menyimpan data: {e}")

def tampilkan_menu():
    """Tampilkan menu utama"""
    print("=" * 40)
    print("         PROGRAM DATA SISWA")
    print("=" * 40)
    print("1. Input Data Siswa")
    print("2. Tampilkan Data Siswa")
    print("3. Exit/keluar")
    print("=" * 40)

def tampilkan_header():
    """Tampilkan header tabel"""
    print(f"{'No':<4} {'Nama':<20} {'Kelas':<10} {'B. Inggris':<12} {'Matematika':<12} {'Fisika':<10} {'Rata-rata':<10}")
    print("-" * 80)

def input_data_siswa(database):
    """Fungsi untuk input data siswa baru"""
    while True:
        clear_screen()
        print("=" * 40)
        print("         INPUT DATA SISWA")
        print("=" * 40)
        
        # Input data
        nama = input("Masukkan Nama: ").strip()
        kelas = input("Masukkan Kelas: ").strip()
        
        # Input nilai dengan validasi
        while True:
            try:
                nilai_inggris = float(input("Masukkan Nilai Bahasa Inggris: "))
                break
            except ValueError:
                print("Input tidak valid! Masukkan angka.")
        
        while True:
            try:
                nilai_matematika = float(input("Masukkan Nilai Matematika: "))
                break
            except ValueError:
                print("Input tidak valid! Masukkan angka.")
        
        while True:
            try:
                nilai_fisika = float(input("Masukkan Nilai Fisika: "))
                break
            except ValueError:
                print("Input tidak valid! Masukkan angka.")
        
        # Buat objek siswa baru
        siswa_baru = Siswa(nama, kelas, nilai_inggris, nilai_matematika, nilai_fisika)
        database.append(siswa_baru)
        
        # Simpan ke file
        simpan_ke_file(database)
        
        print("\nData siswa berhasil disimpan!")
        
        # Tanya apakah ingin input lagi
        lagi = input("Ingin input data lagi? (y/n): ").lower()
        if lagi != 'y':
            break

def tampilkan_data_siswa(database):
    """Fungsi untuk menampilkan data siswa"""
    if not database:
        print("\nBelum ada data siswa!")
        pause()
        return
    
    while True:
        clear_screen()
        print("=" * 40)
        print("         DATA SISWA")
        print("=" * 40)
        print()
        
        tampilkan_header()
        
        for i, siswa in enumerate(database, 1):
            print(f"{i:<4} {siswa.nama:<20} {siswa.kelas:<10} "
                  f"{siswa.nilai_inggris:<12.2f} {siswa.nilai_matematika:<12.2f} "
                  f"{siswa.nilai_fisika:<10.2f} {siswa.hitung_rata_rata():<10.2f}")
        
        print("\n" + "=" * 40)
        print(f"Jumlah Data: {len(database)} siswa")
        print("=" * 40)
        print("1. Hapus Data Siswa")
        print("2. Kembali ke Menu Utama")
        
        pilihan = input("Pilihan (1-2): ").strip()
        
        if pilihan == '1':
            hapus_data_siswa(database)
        elif pilihan == '2':
            break
        else:
            print("Pilihan tidak valid!")

def hapus_data_siswa(database):
    """Fungsi untuk menghapus data siswa"""
    if not database:
        print("Tidak ada data untuk dihapus!")
        pause()
        return
    
    try:
        index = int(input(f"\nMasukkan nomor data yang akan dihapus (1-{len(database)}): "))
        if 1 <= index <= len(database):
            siswa_terhapus = database[index-1]
            konfirmasi = input(f"Data siswa {siswa_terhapus.nama} akan dihapus. Yakin? (y/n): ").lower()
            
            if konfirmasi == 'y':
                database.pop(index-1)
                simpan_ke_file(database)
                print("Data berhasil dihapus!")
            else:
                print("Penghapusan dibatalkan.")
        else:
            print("Nomor data tidak valid!")
    except ValueError:
        print("Input tidak valid!")
    
    pause()

def main():
    """Fungsi utama program"""
    # Baca data dari file
    database = baca_dari_file()
    
    while True:
        clear_screen()
        tampilkan_menu()
        
        pilihan = input("Pilih menu (1-3): ").strip()
        
        if pilihan == '1':
            input_data_siswa(database)
        elif pilihan == '2':
            tampilkan_data_siswa(database)
        elif pilihan == '3':
            print("\nTerima kasih! Program selesai.")
            print(f"Data telah disimpan di file: {FILE_DATABASE}")
            break
        else:
            print("Pilihan tidak valid! Silakan pilih 1-3.")
            pause()

if __name__ == "__main__":

    main()







