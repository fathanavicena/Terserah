import streamlit as st
import pytz
from datetime import datetime

# 1. Konfigurasi Halaman & Styling
st.set_page_config(page_title="Digital Time Shift Cipher", page_icon="🔐")

# 2. Definisi Abjad A-Y (25 huruf)
alphabet = "ABCDEFGHIJKLMN OPQRSTUVWXY".replace(" ", "")

# --- FUNGSI INTI (Tetap Sama) ---
def get_key(h, m):
    return (h + m) % 25

def encrypt(text, h, m):
    key = get_key(h, m)
    result = ""
    for char in text.upper():
        if char in alphabet:
            idx = alphabet.find(char)
            new_idx = (idx + key) % 25
            result += alphabet[new_idx]
        else:
            result += char
    return result, key

def decrypt(text, h, m):
    key = get_key(h, m)
    result = ""
    for char in text.upper():
        if char in alphabet:
            idx = alphabet.find(char)
            new_idx = (idx - key) % 25
            result += alphabet[new_idx]
        else:
            result += char
    return result, key

# --- INTERFACE STREAMLIT ---
st.title("🔐 Digital Time Shift Cipher")
st.write("Sistem enkripsi yang kuncinya ditentukan oleh waktu (Jam + Menit).")

# Sidebar untuk Pengaturan Waktu (Agar Bisa Diubah-ubah)
st.sidebar.header("Pengaturan Waktu")
mode_waktu = st.sidebar.radio("Pilih Mode Waktu:", ("Waktu Sekarang (Auto)", "Input Manual (Custom)"))

if mode_waktu == "Waktu Sekarang (Auto)":
    tz_jkt = pytz.timezone('Asia/Jakarta')
    now = datetime.now(tz_jkt)
    jam_pilihan = now.hour
    menit_pilihan = now.minute
    st.sidebar.info(f"Waktu terdeteksi: {jam_pilihan:02d}:{menit_pilihan:02d}")
else:
    jam_pilihan = st.sidebar.number_input("Masukkan Jam (0-23):", min_value=0, max_value=23, value=12)
    menit_pilihan = st.sidebar.number_input("Masukkan Menit (0-59):", min_value=0, max_value=59, value=0)

# Tab untuk Enkripsi dan Dekripsi
tab1, tab2 = st.tabs(["📤 Enkripsi (Kirim Pesan)", "📥 Dekripsi (Buka Pesan)"])

with tab1:
    st.subheader("Enkripsi")
    pesan_biasa = st.text_area("Masukkan Pesan Teks:", placeholder="Ketik pesan di sini...")
    if st.button("Enkripsi Sekarang"):
        if pesan_biasa:
            hasil, k, h, m = encrypt(pesan_biasa, jam_pilihan, menit_pilihan), get_key(jam_pilihan, menit_pilihan), jam_pilihan, menit_pilihan
            st.success("Pesan Berhasil Dienkripsi!")
            st.code(hasil[0], language=None)
            st.info(f"Kunci (k) = {k} (didapat dari {h}:{m})")
        else:
            st.warning("Mohon masukkan pesan terlebih dahulu.")

with tab2:
    st.subheader("Dekripsi")
    pesan_rahasia = st.text_area("Masukkan Ciphertext (Pesan Rahasia):", placeholder="Paste kode rahasia di sini...")
    if st.button("Dekripsi Sekarang"):
        if pesan_rahasia:
            hasil_dekrip, k = decrypt(pesan_rahasia, jam_pilihan, menit_pilihan)
            st.success("Hasil Dekripsi:")
            st.write(f"**{hasil_dekrip}**")
            st.info(f"Kunci yang digunakan: {k}")
        else:
            st.warning("Mohon masukkan ciphertext terlebih dahulu.")

# Footer
st.divider()
st.caption("Rumus: $k = (Jam + Menit) \pmod{25}$")
