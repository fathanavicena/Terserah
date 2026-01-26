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
    return (h + m) % 25

def get_z_replacement(h):
    return Z_SYMBOLS[h % 24]

def encrypt_logic(text, h, m):
    key = get_dynamic_key(h, m)
    z_char = get_z_replacement(h)
    processed_text = text.upper().replace("Z", z_char)
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
    z_char = get_z_replacement(h)
    result = ""
    for char in text.upper():
        if char in ALPHABET:
            idx = ALPHABET.find(char)
            new_idx = (idx - key) % 25
            result += ALPHABET[new_idx]
        else:
            result += char
    return result.replace(z_char, "Z")

# --- INTERFACE UTAMA ---
st.title("🔐 Digital Clock Cipher (Symbol Edition)")

# Setup Waktu
tz = pytz.timezone('Asia/Jakarta')
now = datetime.now(tz)

# Sidebar hanya untuk pilih Mode
mode_waktu = st.sidebar.radio("Pilih Mode Waktu:", ["Otomatis (Real-time)", "Input Manual"])

# Pemindahan Inputan ke Halaman Utama (Seperti Gambar 2)
if mode_waktu == "Otomatis (Real-time)":
    jam_final = now.hour
    menit_final = now.minute
    st.write(f"🕒 **Waktu Otomatis Aktif:** {jam_final:02d}:{menit_final:02d} WIB")
else:
    col_h, col_m = st.columns(2)
    with col_h:
        jam_final = st.number_input("Input Jam (H)", 0, 23, value=now.hour)
    with col_m:
        menit_final = st.number_input("Input Menit (M)", 0, 59, value=now.minute)

st.write("---")

tab1, tab2 = st.tabs(["Enkripsi", "Dekripsi"])

with tab1:
    st.subheader("Mode Enkripsi")
    msg = st.text_area("Pesan Asli:", placeholder="Ketik pesan Anda...")
    if st.button("Proses Enkripsi"):
        if msg:
            res = encrypt_logic(msg, jam_final, menit_final)
            kunci = get_dynamic_key(jam_final, menit_final)
            
            st.success("Hasil Enkripsi:")
            st.code(res)
            
            # Keterangan Hasil (Detail Waktu & Kunci)
            st.markdown(f"""
            > ✅ **Enkripsi Berhasil!** > 🕒 **Waktu:** {jam_final:02d}:{menit_final:02d} WIB  
            > 🔑 **Key Shift (Mod 25):** {kunci}
            """)
        else:
            st.warning("Masukkan pesan terlebih dahulu.")

with tab2:
    st.subheader("Mode Dekripsi")
    cipher_input = st.text_area("Pesan Terenkripsi:", placeholder="Tempel kode rahasia...")
    if st.button("Proses Dekripsi"):
        if cipher_input:
            plain = decrypt_logic(cipher_input, jam_final, menit_final)
            st.success("Pesan Berhasil Didekripsi:")
            st.subheader(plain)
        else:
            st.warning("Masukkan kode terlebih dahulu.")

st.divider()
st.caption("Dikembangkan dengan Streamlit • Algoritma Digital Clock Cipher")
