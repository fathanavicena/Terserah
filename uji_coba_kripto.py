import streamlit as st
import pytz
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="Digital Clock Cipher Pro", page_icon="🔐")

# 1. Alfabet 25 Karakter (A-Y), Tanpa Z
ALPHABET = "ABCDEFGHIJKLMN OPQRSTUVWXY".replace(" ", "")

# 2. Daftar Simbol Pengganti Z (Total 24 simbol untuk jam 00-23)
Z_SYMBOLS = [
    "!", "@", "#", "$", "%", "^", "&", "*", '"', ":", 
    ";", "/", "\\", "`", "~", "=", "_", "?", "-", "+", 
    "|", "<", ">", "•"
]

def get_dynamic_key(h, m):
    """Menghitung kunci pergeseran berdasarkan (Jam + Menit) mod 25"""
    return (h + m) % 25

def get_z_replacement(h):
    """Mengambil simbol unik untuk Z berdasarkan jam (0-23)"""
    return Z_SYMBOLS[h % 24]

def encrypt_logic(text, h, m):
    key = get_dynamic_key(h, m)
    z_char = get_z_replacement(h)
    
    # Pre-proses: Ubah semua huruf Z menjadi simbol spesifik jam tersebut
    processed_text = text.upper().replace("Z", z_char)
    
    result = ""
    for char in processed_text:
        if char in ALPHABET:
            idx = ALPHABET.find(char)
            new_idx = (idx + key) % 25
            result += ALPHABET[new_idx]
        else:
            # Karakter non-alfabet (termasuk simbol pengganti Z) tetap pada tempatnya
            result += char
    return result

def decrypt_logic(text, h, m):
    key = get_dynamic_key(h, m)
    z_char = get_z_replacement(h)
    
    result = ""
    for char in text.upper():
        if char in ALPHABET:
            idx = ALPHABET.find(char)
            new_idx = (idx - key) % 25
            result += ALPHABET[new_idx]
        else:
            result += char
            
    # Kembalikan simbol jam tersebut menjadi huruf Z kembali
    return result.replace(z_char, "Z")

# --- Interface Streamlit ---
st.title("🔐 Digital Clock Cipher: Hybrid Edition")
st.markdown("Algoritma ini menggunakan waktu sebagai kunci dinamis dan mengganti huruf **Z** dengan simbol unik setiap jamnya.")

# Setup Waktu Real-time
tz = pytz.timezone('Asia/Jakarta')
now = datetime.now(tz)

# Fitur Pilihan Waktu (Otomatis vs Manual)
st.sidebar.header("Pengaturan Waktu")
mode_waktu = st.sidebar.radio("Pilih Mode Waktu:", ["Otomatis (Real-time)", "Input Manual"])

if mode_waktu == "Otomatis (Real-time)":
    jam_final = now.hour
    menit_final = now.minute
    st.sidebar.info(f"Waktu Saat Ini: {jam_final:02d}:{menit_final:02d}")
else:
    jam_final = st.sidebar.number_input("Input Jam (0-23)", 0, 23, value=now.hour)
    menit_final = st.sidebar.number_input("Input Menit (0-59)", 0, 59, value=now.minute)

# Tampilkan informasi simbol Z yang aktif
current_z = get_z_replacement(jam_final)
st.info(f"💡 Pada jam **{jam_final:02d}**, huruf **Z** diproses sebagai simbol: `{current_z}`")

tab1, tab2 = st.tabs(["Enkripsi", "Dekripsi"])

with tab1:
    st.subheader("Mode Enkripsi")
    msg = st.text_area("Pesan Asli:", placeholder="Ketik pesan Anda di sini (Contoh: ZEBRA)...")
    if st.button("Proses Enkripsi"):
        if msg:
            res = encrypt_logic(msg, jam_final, menit_final)
            st.success("Berhasil Enkripsi!")
            st.code(res)
            st.caption(f"Kunci yang digunakan: {(jam_final + menit_final) % 25}")
        else:
            st.warning("Masukkan pesan terlebih dahulu.")

with tab2:
    st.subheader("Mode Dekripsi")
    cipher_input = st.text_area("Pesan Terenkripsi:", placeholder="Tempel kode rahasia di sini...")
    if st.button("Proses Dekripsi"):
        if cipher_input:
            plain = decrypt_logic(cipher_input, jam_final, menit_final)
            st.success("Pesan Berhasil Didekripsi:")
            st.subheader(plain)
        else:
            st.warning("Masukkan kode terlebih dahulu.")

st.divider()
st.caption("Dikembangkan dengan Python & Streamlit • Algoritma Digital Clock Cipher")
