"""Avatar Character Management System - VERSI OOP.
Memakai class, object, attribute, method, inheritance, dan method overriding.
Jalankan: python avatar_oop.py"""
import os

try:  # Tkinter dibungkus agar logika tetap bisa diuji tanpa GUI
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
except ImportError:
    tk = None

FOLDER_PROYEK = os.path.dirname(os.path.abspath(__file__))
FOLDER_ASET = os.path.join(FOLDER_PROYEK, "assets")


# ---------- KELAS INDUK ----------
class KarakterAvatar:
    """Kelas induk: data (attribute) + perilaku (method) satu karakter."""
    ELEMEN = "Umum"
    WARNA = "#888888"

    def __init__(self, nama, kemampuan, deskripsi, gambar=""):
        self.nama = nama
        self.elemen = self.ELEMEN  # elemen ditentukan oleh kelas turunan
        self.kemampuan = kemampuan
        self.deskripsi = deskripsi
        self.gambar = gambar

    def info(self):
        return (f"Nama: {self.nama}\nElemen: {self.elemen}\n"
                f"Kemampuan: {self.kemampuan}\nDeskripsi: {self.deskripsi}")

    def gerakan(self):
        """Dioverride oleh kelas turunan: kalimat aksi khas elemen."""
        return f"{self.nama} memakai kemampuan khusus."

    def gunakan_kemampuan(self):
        return f"{self.gerakan()}\nKemampuan: {self.kemampuan}"

    def path_gambar(self):
        if not self.gambar:
            return ""
        return self.gambar if os.path.isabs(self.gambar) else os.path.join(FOLDER_ASET, self.gambar)

    def muat_gambar(self, ukuran):
        """Return (PhotoImage, None) atau (None, pesan_error).
        Coba Tkinter dulu (PNG/GIF); jika gagal, coba Pillow (bisa baca JPG/WebP)."""
        p = self.path_gambar()
        if not p:
            return None, "Karakter ini belum memiliki gambar."
        if not os.path.isfile(p):
            return None, f"Gambar tidak ditemukan: {os.path.basename(p)}"
        try:
            foto = tk.PhotoImage(file=p)
            f = max(1, max(foto.width(), foto.height()) // ukuran)
            return foto.subsample(f, f), None
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

# ---------- KELAS TURUNAN (inheritance + overriding) ----------
class PengendaliUdara(KarakterAvatar):
    ELEMEN, WARNA = "Udara", "#9ad0f5"

    def gerakan(self):
        return f"{self.nama} melesat dengan glider dan menciptakan pusaran angin."


class PengendaliAir(KarakterAvatar):
    ELEMEN, WARNA = "Air", "#3d7fd6"

    def gerakan(self):
        return f"{self.nama} menarik air menjadi cambuk es dan menyembuhkan luka."

    def gunakan_kemampuan(self):  # override tambahan: air punya efek penyembuhan
        return super().gunakan_kemampuan() + "\nEfek: dapat memulihkan sekutu."


class PengendaliTanah(KarakterAvatar):
    ELEMEN, WARNA = "Tanah", "#a67c4a"

    def gerakan(self):
        return f"{self.nama} menghentakkan bumi, mengangkat dinding batu dan merasakan getaran."


class PengendaliApi(KarakterAvatar):
    ELEMEN, WARNA = "Api", "#e0552b"

    def gerakan(self):
        return f"{self.nama} menyemburkan api dengan semangat dan pengendalian diri."


KELAS_ELEMEN = {k.ELEMEN: k for k in (PengendaliUdara, PengendaliAir, PengendaliTanah, PengendaliApi)}


# ---------- PENGELOLA (tanggung jawab: kumpulan karakter) ----------
class ManajerKarakter:
    def __init__(self):
        self.daftar = [
            PengendaliUdara("Aang", "Airbending dan Avatar State",
                            "Avatar muda dari Suku Udara Selatan yang ceria dan cinta damai.", "aang.png"),
            PengendaliAir("Katara", "Waterbending dan penyembuhan",
                          "Pengendali air dari Suku Air Selatan yang penyayang dan tegas.", "katara.png"),
            PengendaliTanah("Toph", "Earthbending dan seismic sense",
                            "Pengendali tanah buta yang menemukan metalbending.", "toph.png"),
            PengendaliApi("Zuko", "Firebending dan kilat",
                          "Pangeran Negara Api yang berjuang menemukan jati dirinya.", "zuko.png"),
        ]

    def cari(self, kata_kunci):
        return [k for k in self.daftar if kata_kunci.strip().lower() in k.nama.lower()]

    @staticmethod
    def filter_elemen(karakter_list, elemen):
        if elemen == "Semua":
            return list(karakter_list)
        return [k for k in karakter_list if k.elemen == elemen]

    def validasi(self, nama, elemen, kemampuan, deskripsi):
        galat = []
        if not nama.strip():
            galat.append("Nama tidak boleh kosong.")
        elif any(k.nama.lower() == nama.strip().lower() for k in self.daftar):
            galat.append("Nama karakter sudah ada.")
        if elemen not in KELAS_ELEMEN:
            galat.append("Elemen harus dipilih: " + ", ".join(KELAS_ELEMEN) + ".")
        if not kemampuan.strip():
            galat.append("Kemampuan tidak boleh kosong.")
        if not deskripsi.strip():
            galat.append("Deskripsi tidak boleh kosong.")
        return galat

    def tambah(self, nama, elemen, kemampuan, deskripsi, gambar=""):
        """Return (berhasil, galat). Kelas objek dipilih otomatis dari elemen."""
        galat = self.validasi(nama, elemen, kemampuan, deskripsi)
        if galat:
            return False, galat
        kelas = KELAS_ELEMEN[elemen]
        self.daftar.append(kelas(nama.strip(), kemampuan.strip(), deskripsi.strip(), gambar.strip()))
        return True, []


# ---------- GUI (tanggung jawab: tampilan) ----------
class AplikasiAvatar:
    def __init__(self, manajer):
        self.manajer = manajer
        self.root = tk.Tk()
        self.root.title("Avatar Character Management - OOP")
        self.root.configure(bg="#f4ecd8")
        self.kata, self.elem = tk.StringVar(), tk.StringVar(value="Semua")
        atas = tk.Frame(self.root, bg="#f4ecd8")
        atas.pack(fill="x", padx=10, pady=8)
        tk.Label(atas, text="Cari nama:", bg="#f4ecd8").pack(side="left")
        tk.Entry(atas, textvariable=self.kata, width=18).pack(side="left", padx=4)
        tk.Label(atas, text="Elemen:", bg="#f4ecd8").pack(side="left", padx=(10, 0))
        ttk.Combobox(atas, textvariable=self.elem, values=["Semua"] + list(KELAS_ELEMEN),
                     state="readonly", width=8).pack(side="left", padx=4)
        tk.Button(atas, text="Tambah Karakter", command=self.dialog_tambah).pack(side="right")
        self.panel = tk.Frame(self.root, bg="#f4ecd8")
        self.panel.pack(padx=10, pady=5)
        self.pesan = tk.Label(self.root, text="", bg="#f4ecd8", fg="#a00000")
        self.pesan.pack()
        self.kata.trace_add("write", self.perbarui)
        self.elem.trace_add("write", self.perbarui)
        self.perbarui()

    def label_gambar(self, induk, karakter, ukuran):
        foto, galat = karakter.muat_gambar(ukuran)
        if foto:
            lbl = tk.Label(induk, image=foto, bg="white")
            lbl.image = foto
        else:
            lbl = tk.Label(induk, text="[Tanpa gambar]\n" + galat, width=24, height=8, bg="#dddddd",
                           wraplength=170, justify="center")
        return lbl

    def perbarui(self, *_):
        for w in self.panel.winfo_children():
            w.destroy()
        hasil = self.manajer.filter_elemen(self.manajer.cari(self.kata.get()), self.elem.get())
        self.pesan.config(text="" if hasil else "Karakter tidak ditemukan.")
        for i, k in enumerate(hasil):
            kartu = tk.Frame(self.panel, bg="white", highlightthickness=3, highlightbackground=k.WARNA)
            kartu.grid(row=i // 4, column=i % 4, padx=6, pady=6)
            self.label_gambar(kartu, k, 150).pack()
            tk.Label(kartu, text=k.nama, font=("Arial", 13, "bold"), bg="white").pack()
            tk.Label(kartu, text="Elemen: " + k.elemen, bg="white").pack()
            tk.Button(kartu, text="Detail", command=lambda k=k: self.detail(k)).pack(pady=4)

    def detail(self, k):
        j = tk.Toplevel(self.root)
        j.title("Detail " + k.nama)
        j.configure(bg="white", padx=15, pady=15)
        self.label_gambar(j, k, 300).grid(row=0, column=0, rowspan=5, padx=10)
        tk.Label(j, text=k.nama, font=("Arial", 20, "bold"), bg="white", fg=k.WARNA).grid(row=0, column=1, sticky="w")
        tk.Label(j, text="Elemen: " + k.elemen, bg="white").grid(row=1, column=1, sticky="w")
        tk.Label(j, text="Kemampuan: " + k.kemampuan, bg="white").grid(row=2, column=1, sticky="w")
        tk.Label(j, text=k.deskripsi, bg="white", wraplength=300, justify="left").grid(row=3, column=1, sticky="w")
        tk.Button(j, text="Lihat Kemampuan Khusus",
                  command=lambda: messagebox.showinfo("Kemampuan Khusus", k.gunakan_kemampuan(), parent=j)
                  ).grid(row=4, column=1, sticky="w", pady=8)

    def dialog_tambah(self):
        d = tk.Toplevel(self.root)
        d.title("Tambah Karakter")
        isi = {"gambar": ""}
        kolom = {}
        for i, label in enumerate(["Nama", "Kemampuan", "Deskripsi"]):
            tk.Label(d, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=3)
            kolom[label] = tk.Entry(d, width=40)
            kolom[label].grid(row=i, column=1, padx=5)
        tk.Label(d, text="Elemen").grid(row=3, column=0, sticky="e")
        cb = ttk.Combobox(d, values=list(KELAS_ELEMEN), state="readonly")
        cb.grid(row=3, column=1, sticky="w", padx=5)
        lbl = tk.Label(d, text="Gambar: (tidak dipilih -> placeholder)")
        lbl.grid(row=4, column=1, sticky="w")

        def pilih():
            p = filedialog.askopenfilename(parent=d, filetypes=[("Gambar PNG/GIF", "*.png *.gif")])
            if p:
                isi["gambar"] = p
                lbl.config(text="Gambar: " + os.path.basename(p))

        def simpan():
            ok, galat = self.manajer.tambah(kolom["Nama"].get(), cb.get(), kolom["Kemampuan"].get(),
                                            kolom["Deskripsi"].get(), isi["gambar"])
            if ok:
                self.perbarui()
                d.destroy()
            else:
                messagebox.showerror("Data tidak valid", "\n".join(galat), parent=d)

        tk.Button(d, text="Pilih Gambar...", command=pilih).grid(row=5, column=0, pady=8)
        tk.Button(d, text="Simpan", command=simpan).grid(row=5, column=1, sticky="w")

    def jalankan(self):
        self.root.mainloop()


if __name__ == "__main__":
    if tk is None:
        print("Tkinter tidak tersedia. Instal python3-tk (Linux) atau gunakan Python dari python.org.")
    else:
        AplikasiAvatar(ManajerKarakter()).jalankan()
