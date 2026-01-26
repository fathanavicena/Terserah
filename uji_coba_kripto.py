import streamlit as st
import pytz
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="Digital Clock Cipher Pro", page_icon="🔐")

# 1. Alfabet 25 Karakter (A-Y)
ALPHABET = "ABCDEFGHIJKLMN OPQRSTUVWXY".replace(" ", "")

# 2. Daftar Simbol Pengganti Z (Total 24 simbol untuk jam 00-23)
Z_SYMBOLS = [
    "!", "@", "#", "$", "%", "^", "&", "*", '"', ":", 
    ";", "/", "\\", "`", "~", "=", "_", "?", "-", "+", 
    "|", "<", ">", "•"
]

def get_dynamic_key(h, m):
    """Kunci pergeseran: (Jam + Menit) mod 25"""
    return (h + m) % 25

def get_z_replacement(h):
    """Mengambil simbol unik untuk Z berdasarkan jam"""
    return Z_SYMBOLS[h % 24]

def encrypt_logic(text, h, m):
    key = get_dynamic_key(h, m)
    z_char = get_z_replacement(h)
    
    # Ubah Z menjadi simbol spesifik jam tersebut
    processed_text = text.upper().replace("Z", z_char)
    
    result = ""
    for char in processed_text:
        if char in ALPHABET:
            idx = ALPHABET.find(char)
            new_idx = (idx + key) % 25
            result += ALPHABET[new_idx]
        else:
            result += char # Simbol Z-replacement, spasi, dan angka tetap
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
            
    # Kembalikan simbol jam tersebut menjadi Z
    return result.replace(z_char, "Z")

# --- Interface Streamlit ---
st.title("🔐 Digital Clock Cipher: Symbol Edition")
st.markdown("Algoritma ini mengganti huruf **Z** dengan simbol unik yang berbeda setiap jamnya.")

# Setup Waktu
tz = pytz.timezone('Asia/Jakarta')
now = datetime.now(tz)

col1, col2 = st.columns(2)
with col1:
    h = st.number_input("Jam (0-23)", 0, 23, value=now.hour)
with col2:
    m = st.number_input("Menit (0-59)", 0, 59, value=now.minute)

current_z = get_z_replacement(h)
st.info(f"💡 Pada jam **{h:02d}**, huruf **Z** akan berubah menjadi simbol: `{current_z}`")

tab1, tab2 = st.tabs(["Enkripsi", "Dekripsi"])

with tab1:
    msg = st.text_area("Pesan Asli:", placeholder="Ketik pesan (contoh: ZEBRA)...")
    if st.button("Enkripsi"):
        if msg:
            res = encrypt_logic(msg, h, m)
            st.success("Hasil Enkripsi:")
            st.code(res)
        else: st.error("Isi pesan!")

with tab2:
    cipher_input = st.text_area("Pesan Terenkripsi:")
    if st.button("Dekripsi"):
        if cipher_input:
            plain = decrypt_logic(cipher_input, h, m)
            st.success("Pesan Asli:")
            st.subheader(plain)
        else: st.error("Isi kode!")
