# Avatar Character Management System
**Perbandingan Pemrograman Struktural dan OOP** (mini project Programming)

Aplikasi GUI (Tkinter) untuk mengelola karakter *Avatar: The Last Airbender* (Aang, Katara, Toph, Zuko), dibuat dua kali: gaya struktural dan gaya OOP.

## Tujuan pembelajaran
Memahami perbedaan struktural vs OOP, serta class, object, attribute, method, inheritance, dan method overriding.

## Fitur
Daftar karakter (kartu), detail, kemampuan khusus, tambah karakter, cari nama, filter elemen, tampil gambar, validasi input, pesan "tidak ditemukan" dan "data tidak valid". Data tambahan hanya disimpan selama aplikasi berjalan.

## Struktur folder
```
avatar_character_management/
├── avatar_struktural.py
├── avatar_oop.py
├── analisis_perbandingan.md
├── README.md
├── requirements.txt
├── assets/ (aang.png, katara.png, toph.png, zuko.png)
├── tests/test_program.py
└── tools/buat_aset.py
```

## Persyaratan
Python 3.8+ dengan Tkinter. Windows/macOS (python.org) sudah termasuk Tkinter; Ubuntu/Debian: `sudo apt install python3-tk`. Tidak ada library eksternal untuk aplikasi (Pillow hanya opsional, untuk `tools/buat_aset.py`).

## Menjalankan
```
python avatar_struktural.py
python avatar_oop.py
```

## Gambar (penting)
File di `assets/` adalah **ilustrasi placeholder orisinal** (simbol elemen), **bukan gambar resmi** serial, karena gambar resmi berhak cipta dan tidak dapat diunduh/diverifikasi lisensinya di sini. Untuk memakai gambar asli, gunakan hanya gambar yang Anda punya hak/izin pakainya (mis. karya sendiri, atau sumber yang lisensinya Anda verifikasi), lalu simpan sebagai PNG dengan nama yang sama (`aang.png`, dst.) di `assets/`. Tkinter 8.6 membaca PNG dan GIF (bukan JPG). Ukuran besar otomatis diperkecil. Saat menambah karakter, gambar bisa dipilih lewat tombol "Pilih Gambar"; jika kosong atau hilang, tampil kotak placeholder abu-abu bertuliskan pesan.

## Pengujian
Otomatis (logika, tanpa GUI): `python -m unittest discover -s tests -v`

Skenario manual (GUI):
| # | Skenario | Langkah / Input | Hasil diharapkan |
|---|---|---|---|
| 1 | Tampil semua | Buka aplikasi | 4 kartu tampil |
| 2 | Cari ada | Ketik `ka` | Hanya Katara |
| 3 | Cari tidak ada | Ketik `Sokka` | Pesan "Karakter tidak ditemukan." |
| 4 | Tambah baru | Tambah Karakter: Sokka, Air, Strategi, Ahli taktik, Simpan | Kartu ke-5 muncul, placeholder gambar |
| 5 | Kemampuan | Detail Zuko > Lihat Kemampuan Khusus | Dialog teks api + kemampuan |
| 6 | Filter | Pilih elemen Tanah | Hanya Toph |
| 7 | Gambar | Buka Detail Aang | Gambar Aang tampil |
| 8 | Gambar hilang | Ganti nama `assets/zuko.png`, buka ulang | Kartu Zuko tampil pesan "Gambar tidak ditemukan", program tetap jalan |
| 9 | Pilihan tidak valid | Simpan dengan elemen belum dipilih | Dialog error "Elemen harus dipilih" |
| 10 | Data tidak lengkap | Simpan dengan semua kolom kosong | Dialog error 4 pesan; karakter tidak bertambah |

## Perbedaan singkat
Struktural: data dictionary + fungsi, perilaku elemen lewat `if/elif`. OOP: tiap karakter objek dari class turunan yang meng-override `gerakan()`. Detail di `analisis_perbandingan.md`.
