def hitung_determinan_2x2(matriks):
    """
    Menghitung determinan matriks 2x2 secara manual: (a*d) - (b*c)
    """
    a = matriks[0][0]
    b = matriks[0][1]
    c = matriks[1][0]
    d = matriks[1][1]
    return (a * d) - (b * c)

def cari_mod_inverse(n, m=26):
    """
    Mencari Modular Multiplicative Inverse dari determinan terhadap modulo 26.
    Dibutuhkan untuk proses dekripsi Hill Cipher.
    """
    n = n % m
    for x in range(1, m):
        if (n * x) % m == 1:
            return x
    return None

def hitung_invers_matriks_2x2(matriks):
    """
    Mencari invers matriks 2x2 menggunakan metode Adjoin secara manual
    """
    det = hitung_determinan_2x2(matriks)
    det_inv = cari_mod_inverse(det, 26)
    
    if det_inv is None:
        return None
    
    a = matriks[0][0]
    b = matriks[0][1]
    c = matriks[1][0]
    d = matriks[1][1]
    
    adjoin = [
        [d % 26, (-b) % 26],
        [(-c) % 26, a % 26]
    ]
    
   
    invers = [
        [(adjoin[0][0] * det_inv) % 26, (adjoin[0][1] * det_inv) % 26],
        [(adjoin[1][0] * det_inv) % 26, (adjoin[1][1] * det_inv) % 26]
    ]
    return invers

def perkalian_matriks_vektor_2x2(matriks, vektor):
    """
    Mengalikan matriks 2x2 dengan vektor posisi 2x1 secara manual
    """
    hasil_x = (matriks[0][0] * vektor[0] + matriks[0][1] * vektor[1]) % 26
    hasil_y = (matriks[1][0] * vektor[0] + matriks[1][1] * vektor[1]) % 26
    return [hasil_x, hasil_y]
import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# =====================================================================
# 1. FUNGSI MATEMATIKA ALJABAR LINEAR (MANUAL - USER DEFINED)
# =====================================================================

def hitung_determinan_2x2(matriks):
    """Menghitung determinan matriks 2x2 secara manual: (a*d) - (b*c)"""
    a, b = matriks[0][0], matriks[0][1]
    c, d = matriks[1][0], matriks[1][1]
    return (a * d) - (b * c)

def cari_mod_inverse(n, m=26):
    """Mencari Modular Multiplicative Inverse dari determinan modulo m secara manual"""
    n = n % m
    for x in range(1, m):
        if (n * x) % m == 1:
            return x
    return None

def hitung_invers_matriks_2x2(matriks):
    """Mencari invers matriks 2x2 menggunakan metode Adjoin secara manual modulo 26"""
    det = hitung_determinan_2x2(matriks)
    det_inv = cari_mod_inverse(det, 26)
    
    if det_inv is None:
        return None # Matriks tidak memiliki invers modulo 26
        
    a, b = matriks[0][0], matriks[0][1]
    c, d = matriks[1][0], matriks[1][1]
    
    # Matriks Adjoin modulo 26
    adjoin = [
        [d % 26, (-b) % 26],
        [(-c) % 26, a % 26]
    ]
    
    # Invers = (Adjoin * det_inv) % 26
    invers = [
        [(adjoin[0][0] * det_inv) % 26, (adjoin[0][1] * det_inv) % 26],
        [(adjoin[1][0] * det_inv) % 26, (adjoin[1][1] * det_inv) % 26]
    ]
    return invers

def perkalian_matriks_vektor_2x2(matriks, vektor):
    """Mengalikan matriks 2x2 dengan vektor 2x1 secara manual modulo 26"""
    hasil_x = (matriks[0][0] * vektor[0] + matriks[0][1] * vektor[1]) % 26
    hasil_y = (matriks[1][0] * vektor[0] + matriks[1][1] * vektor[1]) % 26
    return [hasil_x, hasil_y]


# =====================================================================
# 2. PROSES PEMROSESAN TEKS (HILL CIPHER)
# =====================================================================

def bersihkan_teks(teks):
    """Mengubah teks menjadi huruf kapital dan hanya menyisakan huruf A-Z"""
    return "".join([karakter.upper() for karakter in teks if karakter.isalpha()])

def enkripsi_hill(plain_text, matriks_kunci):
    """Proses Enkripsi Hill Cipher 2x2"""
    teks_bersih = bersihkan_teks(plain_text)
    
    # Jika jumlah huruf ganjil, tambahkan huruf 'X' di akhir (padding)
    if len(teks_bersih) % 2 != 0:
        teks_bersih += "X"
        
    cipher_text = ""
    # Proses enkripsi per blok 2 huruf (vektor 2x1)
    for i in range(0, len(teks_bersih), 2):
        char1 = teks_bersih[i]
        char2 = teks_bersih[i+1]
        
        # Konversi huruf ke angka (A=0, B=1, ... Z=25)
        vektor = [ord(char1) - 65, ord(char2) - 65]
        
        # Perkalian matriks kunci dengan vektor pesan secara manual
        vektor_hasil = perkalian_matriks_vektor_2x2(matriks_kunci, vektor)
        
        # Konversi kembali angka ke huruf
        cipher_text += chr(vektor_hasil[0] + 65) + chr(vektor_hasil[1] + 65)
        
    return cipher_text

def dekripsi_hill(cipher_text, matriks_kunci):
    """Proses Dekripsi Hill Cipher 2x2"""
    teks_bersih = bersihkan_teks(cipher_text)
    
    # Hitung invers matriks kunci
    invers_kunci = hitung_invers_matriks_2x2(matriks_kunci)
    if invers_kunci is None:
        return None # Pengaman jika kunci tidak valid
        
    plain_text = ""
    # Proses dekripsi per blok 2 huruf
    for i in range(0, len(teks_bersih), 2):
        char1 = teks_bersih[i]
        char2 = teks_bersih[i+1]
        
        vektor = [ord(char1) - 65, ord(char2) - 65]
        
        # Perkalian matriks invers dengan vektor cipher secara manual
        vektor_hasil = perkalian_matriks_vektor_2x2(invers_kunci, vektor)
        
        plain_text += chr(vektor_hasil[0] + 65) + chr(vektor_hasil[1] + 65)
        
    return plain_text


# =====================================================================
# 3. ANTARMUKA APLIKASI DESKTOP (GUI) MENGGUNAKAN TKINTER
# =====================================================================

class AplikasiHillCipher:
    def __init__(self, window):
        self.window = window
        self.window.title("Kriptografi Hill Cipher 2x2 - Aljabar Linear")
        self.window.geometry("550x650")
        self.window.configure(bg="#F4F6F9")
        
        # Styling global
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Header Aplikasi
        header_frame = tk.Frame(window, bg="#2C3E50", height=70)
        header_frame.pack(fill="x")
        
        label_judul = tk.Label(header_frame, text="HILL CIPHER 2x2 SIMULATOR", 
                               fg="white", bg="#2C3E50", font=("Helvetica", 14, "bold"))
        label_judul.pack(pady=15)
        
        # Frame Konten Utama
        konten_frame = tk.Frame(window, bg="#F4F6F9", padx=20, pady=10)
        konten_frame.pack(fill="both", expand=True)
        
        # --- INPUT MATRIKS KUNCI ---
        lbl_kunci = tk.Label(konten_frame, text="1. Masukkan Matriks Kunci (2x2):", 
                             bg="#F4F6F9", font=("Helvetica", 11, "bold"))
        lbl_kunci.grid(row=0, column=0, columnspan=4, sticky="w", pady=(10, 5))
        
        # Kotak grid input matriks
        self.k11 = tk.Entry(konten_frame, width=5, font=("Helvetica", 11), justify="center")
        self.k12 = tk.Entry(konten_frame, width=5, font=("Helvetica", 11), justify="center")
        self.k21 = tk.Entry(konten_frame, width=5, font=("Helvetica", 11), justify="center")
        self.k22 = tk.Entry(konten_frame, width=5, font=("Helvetica", 11), justify="center")
        
        self.k11.grid(row=1, column=0, padx=5, pady=5)
        self.k12.grid(row=1, column=1, padx=5, pady=5)
        self.k21.grid(row=2, column=0, padx=5, pady=5)
        self.k22.grid(row=2, column=1, padx=5, pady=5)
        
        
        self.k11.insert(0, "3")
        self.k12.insert(0, "3")
        self.k21.insert(0, "2")
        self.k22.insert(0, "5")
        
       
        btn_cek_kunci = tk.Button(konten_frame, text="Verifikasi Kunci", command=self.verifikasi_kunci_input,
                                  bg="#2980B9", fg="white", font=("Helvetica", 10, "bold"), padx=10)
        btn_cek_kunci.grid(row=1, column=2, rowspan=2, columnspan=2, padx=15)
        
       
        lbl_pesan = tk.Label(konten_frame, text="2. Tulis Pesan Anda:", 
                             bg="#F4F6F9", font=("Helvetica", 11, "bold"))
        lbl_pesan.grid(row=3, column=0, columnspan=4, sticky="w", pady=(20, 5))
        
        self.input_pesan = tk.Text(konten_frame, height=4, width=55, font=("Helvetica", 10))
        self.input_pesan.grid(row=4, column=0, columnspan=4, pady=5)
        
       
        tombol_frame = tk.Frame(konten_frame, bg="#F4F6F9")
        tombol_frame.grid(row=5, column=0, columnspan=4, pady=15)
        
        btn_enkripsi = tk.Button(tombol_frame, text="🔒 ENKRIPSI", command=self.proses_enkripsi,
                                 bg="#27AE60", fg="white", font=("Helvetica", 10, "bold"), width=15, pady=5)
        btn_enkripsi.pack(side="left", padx=10)
        
        btn_dekripsi = tk.Button(tombol_frame, text="🔓 DEKRIPSI", command=self.proses_dekripsi,
                                 bg="#E74C3C", fg="white", font=("Helvetica", 10, "bold"), width=15, pady=5)
        btn_dekripsi.pack(side="left", padx=10)
        
       
        lbl_hasil = tk.Label(konten_frame, text="3. Hasil Keluaran (Output):", 
                             bg="#F4F6F9", font=("Helvetica", 11, "bold"))
        lbl_hasil.grid(row=6, column=0, columnspan=4, sticky="w", pady=(15, 5))
        
        self.output_hasil = tk.Text(konten_frame, height=5, width=55, font=("Helvetica", 10), bg="#EAEDED")
        self.output_hasil.grid(row=7, column=0, columnspan=4, pady=5)
        
        
        footer_label = tk.Label(window, text=f"Waktu Sistem: {datetime.datetime.now().strftime('%Y-%m-%d')}", 
                                bg="#BDC3C7", fg="#2C3E50", font=("Helvetica", 9, "italic"))
        footer_label.pack(side="bottom", fill="x")

    def ambil_matriks_dari_gui(self):
        """Membaca nilai entri input dari GUI dan menyusunnya menjadi matriks list 2D"""
        try:
            kunci = [
                [int(self.k11.get()), int(self.k12.get())],
                [int(self.k21.get()), int(self.k22.get())]
            ]
            return kunci
        except ValueError:
            messagebox.showerror("Error Input", "Semua elemen matriks kunci harus berupa angka bulat!")
            return None

    def verifikasi_kunci_input(self):
        """Memeriksa kelayakan matriks kunci di layar"""
        kunci = self.ambil_matriks_dari_gui()
        if kunci is None:
            return False
            
        det = hitung_determinan_2x2(kunci)
        det_mod = det % 26
        det_inv = cari_mod_inverse(det_mod, 26)
        
        info_teks = f"Analisis Kunci:\n Determinan: {det}\n Determinan Mod 26: {det_mod}\n"
        
        if det_mod == 0:
            info_teks += "Status: TIDAK VALID!\n(Determinan modulo 26 bernilai 0, matriks singular / tidak punya invers)"
            messagebox.showwarning("Verifikasi Kunci", info_teks)
            return False
        elif det_inv is None:
            info_teks += "Status: TIDAK VALID!\n(Determinan tidak relatif prima dengan 26, invers modular tidak ditemukan)"
            messagebox.showwarning("Verifikasi Kunci", info_teks)
            return False
        else:
            info_teks += f" Mod Invers Determinan: {det_inv}\nStatus: VALID DAN AMAN DIGUNAKAN!"
            messagebox.showinfo("Verifikasi Kunci", info_teks)
            return True

    def proses_enkripsi(self):
        kunci = self.ambil_matriks_dari_gui()
        if kunci is None:
            return
            
        
        det = hitung_determinan_2x2(kunci)
        if cari_mod_inverse(det % 26, 26) is None:
            messagebox.showerror("Kunci Salah", "Gunakan kunci yang valid terlebih dahulu (klik Verifikasi Kunci)!")
            return
            
        pesan_masuk = self.input_pesan.get("1.0", tk.END).strip()
        if not pesan_masuk:
            messagebox.showwarning("Input Kosong", "Tuliskan pesan teks yang ingin dienkripsi!")
            return
            
        hasil_ciper = enkripsi_hill(pesan_masuk, kunci)
        
        self.output_hasil.delete("1.0", tk.END)
        self.output_hasil.insert(tk.END, f"Teks Asli: {bersihkan_teks(pesan_masuk)}\n")
        self.output_hasil.insert(tk.END, f"Hasil Enkripsi (Ciphertext): {hasil_ciper}\n")

    def proses_dekripsi(self):
        kunci = self.ambil_matriks_dari_gui()
        if kunci is None:
            return
            
        det = hitung_determinan_2x2(kunci)
        if cari_mod_inverse(det % 26, 26) is None:
            messagebox.showerror("Kunci Salah", "Gunakan kunci yang valid terlebih dahulu!")
            return
            
        pesan_masuk = self.input_pesan.get("1.0", tk.END).strip()
        if not pesan_masuk:
            messagebox.showwarning("Input Kosong", "Tuliskan cipherteks yang ingin didekripsi!")
            return
            
        hasil_plain = dekripsi_hill(pesan_masuk, kunci)
        
        self.output_hasil.delete("1.0", tk.END)
        self.output_hasil.insert(tk.END, f"Ciphertext: {bersihkan_teks(pesan_masuk)}\n")
        self.output_hasil.insert(tk.END, f"Hasil Dekripsi (Plaintext): {hasil_plain}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiHillCipher(root)
    root.mainloop()
