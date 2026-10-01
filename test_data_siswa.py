import os
import tempfile
import unittest
from data_siswa import Siswa, baca_dari_file, simpan_ke_file, ekspor_ke_csv, ekspor_ke_json


class TestSiswaModel(unittest.TestCase):
    def test_perhitungan_rata_rata(self):
        siswa = Siswa("Andi", "10-IPA", 80.0, 90.0, 70.0)
        self.assertAlmostEqual(siswa.hitung_rata_rata(), 80.0, places=2)

    def test_predikat_nilai(self):
        self.assertEqual(Siswa("A", "10", 95, 92, 90).predikat(), "A")
        self.assertEqual(Siswa("B", "10", 82, 85, 80).predikat(), "B")
        self.assertEqual(Siswa("C", "10", 72, 75, 70).predikat(), "C")
        self.assertEqual(Siswa("D", "10", 62, 65, 60).predikat(), "D")
        self.assertEqual(Siswa("E", "10", 50, 40, 55).predikat(), "E")

    def test_status_kelulusan_kkm(self):
        siswa_lulus = Siswa("Lulus", "10", 75.0, 75.0, 75.0)
        self.assertEqual(siswa_lulus.status_kelulusan(), "Lulus")

        siswa_remedial = Siswa("Remed", "10", 74.0, 70.0, 72.0)
        self.assertEqual(siswa_remedial.status_kelulusan(), "Remedial")

    def test_serialisasi_dan_deserialisasi_string(self):
        siswa = Siswa("Budi Santoso", "11-B", 85.5, 90.0, 88.25)
        raw_str = siswa.ke_string()
        self.assertEqual(raw_str, "Budi Santoso|11-B|85.50|90.00|88.25")

        siswa_pulih = Siswa.dari_string(raw_str)
        self.assertIsNotNone(siswa_pulih)
        self.assertEqual(siswa_pulih.nama, "Budi Santoso")
        self.assertEqual(siswa_pulih.kelas, "11-B")
        self.assertAlmostEqual(siswa_pulih.nilai_inggris, 85.5)
        self.assertAlmostEqual(siswa_pulih.nilai_matematika, 90.0)
        self.assertAlmostEqual(siswa_pulih.nilai_fisika, 88.25)

    def test_sanitasi_karakter_pipe(self):
        siswa = Siswa("Nama|Palsu", "Kelas|10", 80, 80, 80)
        raw_str = siswa.ke_string()
        self.assertNotIn("Nama|Palsu", raw_str)
        self.assertIn("Nama/Palsu", raw_str)

    def test_dari_string_format_salah(self):
        self.assertIsNone(Siswa.dari_string("baris|tidak|lengkap"))
        self.assertIsNone(Siswa.dari_string("Nama|Kelas|bukan_angka|80|90"))

    def test_ke_dict(self):
        siswa = Siswa("Citra", "12-C", 90.0, 95.0, 92.0)
        data_dict = siswa.ke_dict()
        self.assertEqual(data_dict["nama"], "Citra")
        self.assertEqual(data_dict["kelas"], "12-C")
        self.assertEqual(data_dict["predikat"], "A")
        self.assertEqual(data_dict["status"], "Lulus")


class TestPersistensiDanEkspor(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        self.temp_file.close()
        self.daftar_siswa = [
            Siswa("Ahmad", "10-A", 85.0, 90.0, 88.0),
            Siswa("Budi", "10-A", 70.0, 72.0, 68.0),
            Siswa("Citra", "10-B", 95.0, 96.0, 94.0)
        ]

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_simpan_dan_baca_file(self):
        sukses = simpan_ke_file(self.daftar_siswa, filepath=self.temp_file.name)
        self.assertTrue(sukses)

        muat = baca_dari_file(filepath=self.temp_file.name, verbose=False)
        self.assertEqual(len(muat), 3)
        self.assertEqual(muat[0].nama, "Ahmad")
        self.assertEqual(muat[2].nama, "Citra")

    def test_ekspor_csv(self):
        csv_path = self.temp_file.name + ".csv"
        try:
            sukses, _ = ekspor_ke_csv(self.daftar_siswa, filepath=csv_path)
            self.assertTrue(sukses)
            self.assertTrue(os.path.exists(csv_path))
            with open(csv_path, "r", encoding="utf-8") as f:
                konten = f.read()
                self.assertIn("Ahmad", konten)
                self.assertIn("Rata-rata", konten)
        finally:
            if os.path.exists(csv_path):
                os.remove(csv_path)

    def test_ekspor_json(self):
        json_path = self.temp_file.name + ".json"
        try:
            sukses, _ = ekspor_ke_json(self.daftar_siswa, filepath=json_path)
            self.assertTrue(sukses)
            self.assertTrue(os.path.exists(json_path))
            with open(json_path, "r", encoding="utf-8") as f:
                konten = f.read()
                self.assertIn("total_siswa", konten)
                self.assertIn("Citra", konten)
        finally:
            if os.path.exists(json_path):
                os.remove(json_path)


if __name__ == "__main__":
    unittest.main()
