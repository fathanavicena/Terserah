import streamlit as st
import pytz
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="Digital Clock Cipher", page_icon="🔐")

# Alfabet 25 Karakter (A-Y), Tanpa Z
ALPHABET = "ABCDEFGHIJKLMN OPQRSTUVWXY".replace(" ", "")

def get_dynamic_key(h, m):
    """Menghitung kunci berdasarkan (Jam + Menit) mod 25"""
    return (h + m) % 25

def encrypt_logic(text, h, m):
    key = get_dynamic_key(h, m)
    # Transformasi otomatis: Semua Z diubah menjadi Y sebelum enkripsi
    processed_text = text.upper().replace("Z", "Y")
    result = ""
    for char in processed_text:
        if char in ALPHABET:
            idx = ALPHABET.find(char)
            new_idx = (idx + key) % 25
            result += ALPHABET[new_idx]
        else:
            result += char
    return result

def decrypt_logic(text, h, m):
    key = get_dynamic_key(h, m)
    result = ""
    for char in text.upper():
        if char in ALPHABET:
            idx = ALPHABET.find(char)
            new_idx = (idx - key) % 25
            result += ALPHABET[new_idx]
        else:
            result += char
    return result

# --- Tampilan Streamlit ---
st.title("🔐 Digital Clock Cipher (No-Z Edition)")
st.markdown("""
Aplikasi ini menggunakan waktu (Jam & Menit) sebagai kunci enkripsi dinamis. 
**Aturan Khusus:** Alfabet hanya terdiri dari 25 karakter (A-Y). Huruf **Z** otomatis diubah menjadi **Y** untuk menjaga integritas algoritma mod 25.
""")

# Setup Waktu Lokal
tz = pytz.timezone('Asia/Jakarta')
now = datetime.now(tz)

col1, col2 = st.columns(2)
with col1:
    h = st.number_input("Input Jam (H)", 0, 23, value=now.hour)
with col2:
    m = st.number_input("Input Menit (M)", 0, 59, value=now.minute)

tab1, tab2 = st.tabs(["Enkripsi", "Dekripsi"])

with tab1:
    msg = st.text_area("Pesan Asli:", placeholder="Ketik pesan di sini (Contoh: ZEBRA)...")
    if st.button("Proses Enkripsi"):
        if msg:
            ciphertext = encrypt_logic(msg, h, m)
            st.success(f"Hasil Enkripsi (Kunci K={(h+m)%25}):")
            st.code(ciphertext)
        else:
            st.error("Isi pesan terlebih dahulu!")

with tab2:
    cipher_input = st.text_area("Pesan Terenkripsi:")
    if st.button("Proses Dekripsi"):
        if cipher_input:
            plain_text = decrypt_logic(cipher_input, h, m)
            st.success("Pesan Berhasil Didekripsi:")
            st.subheader(plain_text)
        else:
            st.error("Isi kode rahasia terlebih dahulu!")

st.divider()
st.caption("Dikembangkan dengan Python & Streamlit")
