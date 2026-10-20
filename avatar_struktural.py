"""Avatar Character Management System - VERSI STRUKTURAL.
Tanpa class sebagai struktur utama: hanya variabel, list, dictionary, fungsi,
perulangan, dan percabangan. Jalankan: python avatar_struktural.py"""
import os

try:  # Tkinter dibungkus agar logika tetap bisa diuji tanpa GUI
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
except ImportError:
    tk = None

FOLDER_PROYEK = os.path.dirname(os.path.abspath(__file__))  # path relatif ke proyek
FOLDER_ASET = os.path.join(FOLDER_PROYEK, "assets")
DAFTAR_ELEMEN = ["Udara", "Air", "Tanah", "Api"]
WARNA_ELEMEN = {"Udara": "#9ad0f5", "Air": "#3d7fd6", "Tanah": "#a67c4a", "Api": "#e0552b"}

# ---------- DATA: list berisi dictionary (penyimpanan data struktural) ----------
daftar_karakter = [
    {"nama": "Aang", "elemen": "Udara", "kemampuan": "Airbending dan Avatar State",
     "deskripsi": "Avatar muda dari Suku Udara Selatan yang ceria dan cinta damai.", "gambar": "aang.png"},
    {"nama": "Katara", "elemen": "Air", "kemampuan": "Waterbending dan penyembuhan",
     "deskripsi": "Pengendali air dari Suku Air Selatan yang penyayang dan tegas.", "gambar": "katara.png"},
    {"nama": "Toph", "elemen": "Tanah", "kemampuan": "Earthbending dan seismic sense",
     "deskripsi": "Pengendali tanah buta yang menemukan metalbending.", "gambar": "toph.png"},
    {"nama": "Zuko", "elemen": "Api", "kemampuan": "Firebending dan kilat",
     "deskripsi": "Pangeran Negara Api yang berjuang menemukan jati dirinya.", "gambar": "zuko.png"},
]


# ---------- FUNGSI LOGIKA (tanpa GUI) ----------
def cari_karakter(daftar, kata_kunci):
    """Cari berdasarkan nama (tidak peka huruf besar/kecil)."""
    hasil = []
    for k in daftar:  # perulangan
        if kata_kunci.strip().lower() in k["nama"].lower():  # percabangan
            hasil.append(k)
    return hasil


def filter_elemen(daftar, elemen):
    """Filter berdasarkan elemen; 'Semua' mengembalikan seluruh daftar."""
    if elemen == "Semua":
        return list(daftar)
    return [k for k in daftar if k["elemen"] == elemen]


def kemampuan_khusus(karakter):
    """Perilaku kemampuan dipilih dengan if/elif berdasarkan elemen (ciri struktural)."""
    n, e = karakter["nama"], karakter["elemen"]
    if e == "Udara":
        pesan = f"{n} melesat dengan glider dan menciptakan pusaran angin."
    elif e == "Air":
        pesan = f"{n} menarik air menjadi cambuk es dan menyembuhkan luka."
    elif e == "Tanah":
        pesan = f"{n} menghentakkan bumi, mengangkat dinding batu dan merasakan getaran."
    elif e == "Api":
        pesan = f"{n} menyemburkan api dengan semangat dan pengendalian diri."
    else:  # elemen tak dikenal
        pesan = f"{n} memakai kemampuan khusus."
    return f"{pesan}\nKemampuan: {karakter['kemampuan']}"


def validasi_karakter_baru(nama, elemen, kemampuan, deskripsi, daftar):
    """Kembalikan daftar pesan kesalahan; kosong berarti valid."""
    galat = []
    if not nama.strip():
        galat.append("Nama tidak boleh kosong.")
    elif any(k["nama"].lower() == nama.strip().lower() for k in daftar):
        galat.append("Nama karakter sudah ada.")
    if elemen not in DAFTAR_ELEMEN:
        galat.append("Elemen harus dipilih: " + ", ".join(DAFTAR_ELEMEN) + ".")
    if not kemampuan.strip():
        galat.append("Kemampuan tidak boleh kosong.")
    if not deskripsi.strip():
        galat.append("Deskripsi tidak boleh kosong.")
    return galat


def tambah_karakter(daftar, nama, elemen, kemampuan, deskripsi, gambar=""):
    """Tambahkan karakter jika valid. Return (berhasil, daftar_pesan_galat)."""
    galat = validasi_karakter_baru(nama, elemen, kemampuan, deskripsi, daftar)
    if galat:
        return False, galat
    daftar.append({"nama": nama.strip(), "elemen": elemen, "kemampuan": kemampuan.strip(),
                   "deskripsi": deskripsi.strip(), "gambar": gambar.strip()})
    return True, []


def path_gambar(karakter):
    """Path gambar: nama file -> folder assets; path absolut dipakai apa adanya."""
    if not karakter["gambar"]:
        return ""
    if os.path.isabs(karakter["gambar"]):
        return karakter["gambar"]
    return os.path.join(FOLDER_ASET, karakter["gambar"])


def muat_gambar(karakter, ukuran):
    """Return (PhotoImage, None) atau (None, pesan_error).
    Coba Tkinter dulu (PNG/GIF); jika gagal, coba Pillow (bisa baca JPG/WebP)."""
    p = path_gambar(karakter)
    if not p:
        return None, "Karakter ini belum memiliki gambar."
    if not os.path.isfile(p):
        return None, f"Gambar tidak ditemukan: {os.path.basename(p)}"
    try:
        foto = tk.PhotoImage(file=p)  # Tkinter 8.6 mendukung PNG/GIF
        faktor = max(1, max(foto.width(), foto.height()) // ukuran)
        return foto.subsample(faktor, faktor), None
    except Exception as e1:
        print("PhotoImage gagal untuk", p, "->", e1)
        try:
            from PIL import Image, ImageTk  # opsional: pip install pillow
            img = Image.open(p).convert("RGBA")
            img.thumbnail((ukuran, ukuran))
            return ImageTk.PhotoImage(img), None
        except Exception as e2:
            print("Pillow juga gagal untuk", p, "->", e2)
            return None, f"Gambar gagal dimuat: {os.path.basename(p)} (pasang Pillow atau gunakan PNG asli)"


# ---------- FUNGSI GUI ----------
def buat_label_gambar(induk, karakter, ukuran):
    foto, galat = muat_gambar(karakter, ukuran)
    if foto:
        lbl = tk.Label(induk, image=foto, bg="white")
        lbl.image = foto  # simpan referensi agar tidak dihapus Python
    else:
        lbl = tk.Label(induk, text="[Tanpa gambar]\n" + galat, width=24, height=8, bg="#dddddd",
                       wraplength=170, justify="center")
    return lbl


def tampilkan_detail(root, karakter):
    jendela = tk.Toplevel(root)
    jendela.title("Detail " + karakter["nama"])
    jendela.configure(bg="white", padx=15, pady=15)
    buat_label_gambar(jendela, karakter, 300).grid(row=0, column=0, rowspan=5, padx=10)
    tk.Label(jendela, text=karakter["nama"], font=("Arial", 20, "bold"), bg="white",
             fg=WARNA_ELEMEN.get(karakter["elemen"], "black")).grid(row=0, column=1, sticky="w")
    tk.Label(jendela, text="Elemen: " + karakter["elemen"], bg="white").grid(row=1, column=1, sticky="w")
    tk.Label(jendela, text="Kemampuan: " + karakter["kemampuan"], bg="white").grid(row=2, column=1, sticky="w")
    tk.Label(jendela, text=karakter["deskripsi"], bg="white", wraplength=300, justify="left").grid(row=3, column=1, sticky="w")
    tk.Button(jendela, text="Lihat Kemampuan Khusus",
              command=lambda: messagebox.showinfo("Kemampuan Khusus", kemampuan_khusus(karakter), parent=jendela)
              ).grid(row=4, column=1, sticky="w", pady=8)


def dialog_tambah(root, perbarui):
    d = tk.Toplevel(root)
    d.title("Tambah Karakter")
    isi = {"gambar": ""}
    kolom = {}
    for i, label in enumerate(["Nama", "Kemampuan", "Deskripsi"]):
        tk.Label(d, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=3)
        kolom[label] = tk.Entry(d, width=40)
        kolom[label].grid(row=i, column=1, padx=5)
    tk.Label(d, text="Elemen").grid(row=3, column=0, sticky="e")
    cb = ttk.Combobox(d, values=DAFTAR_ELEMEN, state="readonly")
    cb.grid(row=3, column=1, sticky="w", padx=5)
    lbl_gambar = tk.Label(d, text="Gambar: (tidak dipilih -> placeholder)")
    lbl_gambar.grid(row=4, column=1, sticky="w")

    def pilih_gambar():
        p = filedialog.askopenfilename(parent=d, filetypes=[("Gambar PNG/GIF", "*.png *.gif")])
        if p:
            isi["gambar"] = p
            lbl_gambar.config(text="Gambar: " + os.path.basename(p))

    def simpan():
        ok, galat = tambah_karakter(daftar_karakter, kolom["Nama"].get(), cb.get(),
                                    kolom["Kemampuan"].get(), kolom["Deskripsi"].get(), isi["gambar"])
        if ok:
            perbarui()
            d.destroy()
        else:
            messagebox.showerror("Data tidak valid", "\n".join(galat), parent=d)

    tk.Button(d, text="Pilih Gambar...", command=pilih_gambar).grid(row=5, column=0, pady=8)
    tk.Button(d, text="Simpan", command=simpan).grid(row=5, column=1, sticky="w")


def jalankan_gui():
    root = tk.Tk()
    root.title("Avatar Character Management - Struktural")
    root.configure(bg="#f4ecd8")
    atas = tk.Frame(root, bg="#f4ecd8")
    atas.pack(fill="x", padx=10, pady=8)
    kata = tk.StringVar()
    elem = tk.StringVar(value="Semua")
    tk.Label(atas, text="Cari nama:", bg="#f4ecd8").pack(side="left")
    tk.Entry(atas, textvariable=kata, width=18).pack(side="left", padx=4)
    tk.Label(atas, text="Elemen:", bg="#f4ecd8").pack(side="left", padx=(10, 0))
    ttk.Combobox(atas, textvariable=elem, values=["Semua"] + DAFTAR_ELEMEN, state="readonly", width=8).pack(side="left", padx=4)
    panel = tk.Frame(root, bg="#f4ecd8")
    panel.pack(padx=10, pady=5)
    pesan = tk.Label(root, text="", bg="#f4ecd8", fg="#a00000")
    pesan.pack()

    def perbarui(*_):
        for w in panel.winfo_children():
            w.destroy()
        hasil = filter_elemen(cari_karakter(daftar_karakter, kata.get()), elem.get())
        pesan.config(text="" if hasil else "Karakter tidak ditemukan.")
        for i, k in enumerate(hasil):  # setiap karakter = satu kartu
            kartu = tk.Frame(panel, bg="white", highlightthickness=3,
                             highlightbackground=WARNA_ELEMEN.get(k["elemen"], "gray"))
            kartu.grid(row=i // 4, column=i % 4, padx=6, pady=6)
            buat_label_gambar(kartu, k, 150).pack()
            tk.Label(kartu, text=k["nama"], font=("Arial", 13, "bold"), bg="white").pack()
            tk.Label(kartu, text="Elemen: " + k["elemen"], bg="white").pack()
            tk.Button(kartu, text="Detail", command=lambda k=k: tampilkan_detail(root, k)).pack(pady=4)

    tk.Button(atas, text="Tambah Karakter", command=lambda: dialog_tambah(root, perbarui)).pack(side="right")
    kata.trace_add("write", perbarui)
    elem.trace_add("write", perbarui)
    perbarui()
    root.mainloop()


if __name__ == "__main__":
    if tk is None:
        print("Tkinter tidak tersedia. Instal python3-tk (Linux) atau gunakan Python dari python.org.")
    else:
        jalankan_gui()
