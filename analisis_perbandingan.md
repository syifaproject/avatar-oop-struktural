# Analisis Perbandingan: Pemrograman Struktural vs OOP

Proyek: **Avatar Character Management System**. Kedua versi punya fitur yang sama: daftar karakter, detail, kemampuan khusus, tambah, cari nama, filter elemen, tampil gambar, validasi input, dan pesan error.

## 1. Bagian struktural (`avatar_struktural.py`)
- **Data**: `daftar_karakter` = list berisi dictionary.
- **Fungsi mandiri**: `cari_karakter()`, `filter_elemen()`, `tambah_karakter()`, `validasi_karakter_baru()`, `kemampuan_khusus()`, `muat_gambar()`.
- **Perulangan & percabangan**: `for` pada pencarian, `if/elif` pada `kemampuan_khusus()`.

```python
def kemampuan_khusus(karakter):
    if karakter["elemen"] == "Udara":
        pesan = ...
    elif karakter["elemen"] == "Air":
        pesan = ...
```

## 2. Class, object, attribute, method (`avatar_oop.py`)
- **Class**: `KarakterAvatar`, `ManajerKarakter`, `AplikasiAvatar`.
- **Object**: `PengendaliUdara("Aang", ...)`, dst.
- **Attribute**: `nama`, `elemen`, `kemampuan`, `deskripsi`, `gambar`.
- **Method**: `info()`, `gerakan()`, `gunakan_kemampuan()`, `muat_gambar()`.

## 3. Inheritance dan method overriding
```python
class PengendaliAir(KarakterAvatar):
    ELEMEN = "Air"
    def gerakan(self):                      # overriding
        return f"{self.nama} menarik air menjadi cambuk es ..."
    def gunakan_kemampuan(self):            # overriding + super()
        return super().gunakan_kemampuan() + "\nEfek: dapat memulihkan sekutu."
```
Kelas turunan mewarisi atribut dan `info()` dari induk, tetapi perilakunya berbeda (Air punya efek penyembuhan yang tidak dimiliki yang lain). Ini diuji di `test_overriding`.

## 4. Perbedaan penyimpanan dan pengelolaan data
| Aspek | Struktural | OOP |
|---|---|---|
| Bentuk data | dictionary `{"nama": ...}` | objek `karakter.nama` |
| Penyimpanan | list global `daftar_karakter` | list di dalam `ManajerKarakter` |
| Data & aksi | terpisah (data di satu tempat, fungsi di tempat lain) | menyatu dalam class |

## 5. Alur program dan tanggung jawab
- **Struktural**: program mengalir dari atas ke bawah; fungsi menerima dictionary sebagai parameter.
- **OOP**: tanggung jawab dibagi: karakter (perilaku sendiri), manajer (cari/filter/tambah/validasi), aplikasi (tampilan).

## 6. Cara menambah karakter baru
- Struktural: `tambah_karakter(daftar, nama, elemen, ...)` menambahkan dictionary baru. Perilaku kemampuan tetap diatur `if/elif`.
- OOP: `ManajerKarakter.tambah()` memilih kelas dari `KELAS_ELEMEN[elemen]` lalu membuat objek, sehingga karakter baru otomatis punya perilaku elemennya.

## 7. Kelebihan dan kekurangan
| | Kelebihan | Kekurangan |
|---|---|---|
| Struktural | Sederhana, cepat dipahami pemula, kode lebih pendek | Perilaku per elemen tersebar di `if/elif`; makin banyak elemen makin panjang; data global |
| OOP | Perilaku terkait elemen terkumpul rapi, mudah diperluas, tanggung jawab jelas | Lebih banyak konsep dan kode awal; terasa berlebihan untuk program sangat kecil |

## 8. Contoh perubahan fitur
**Menambah elemen baru "Petir"** (misal untuk Azula).
- Struktural: tambah `"Petir"` di `DAFTAR_ELEMEN`, `WARNA_ELEMEN`, dan satu cabang `elif` di `kemampuan_khusus()` (tiga tempat berbeda).
- OOP: buat satu class `PengendaliPetir` dan daftarkan di `KELAS_ELEMEN`. Kode lain tidak berubah. **OOP lebih mudah** untuk perubahan jenis ini.

**Mengubah format cetak sederhana** (mis. urutan daftar): struktural cukup ubah satu fungsi dan hasilnya lebih langsung.

## 9. Perbandingan fitur setara
| Fitur | Struktural | OOP |
|---|---|---|
| Daftar karakter | `perbarui()` di `jalankan_gui` | `AplikasiAvatar.perbarui()` |
| Detail | `tampilkan_detail()` | `AplikasiAvatar.detail()` |
| Kemampuan khusus | `kemampuan_khusus()` | `gunakan_kemampuan()` |
| Tambah | `tambah_karakter()` | `ManajerKarakter.tambah()` |
| Cari nama | `cari_karakter()` | `ManajerKarakter.cari()` |
| Filter elemen | `filter_elemen()` | `ManajerKarakter.filter_elemen()` |
| Gambar | `muat_gambar()` | `KarakterAvatar.muat_gambar()` |
| Validasi | `validasi_karakter_baru()` | `ManajerKarakter.validasi()` |

`test_hasil_sama` memeriksa bahwa kedua versi menghasilkan daftar, filter, dan teks kemampuan yang sama.
