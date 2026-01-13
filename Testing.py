import streamlit as st
import datetime

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Digital Clock Cipher", page_icon="🔐")

# --- Fungsi Logika ---
def process_cipher(text, hour, minute, mode="Enkripsi"):
    # Alfabet tanpa huruf Z (25 karakter)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXY"
    shift = (hour + minute) % 25
    
    if mode == "Dekripsi":
        shift = -shift
        
    result = ""
    # Normalisasi teks ke uppercase dan ubah Z menjadi Y sesuai aturan di gambar
    text = text.upper().replace('Z', 'Y')
    
    for char in text:
        if char in alphabet:
            idx = alphabet.find(char)
            new_idx = (idx + shift) % 25
            result += alphabet[new_idx]
        else:
            result += char # Untuk spasi atau simbol
            
    return result

# --- Tampilan UI (Streamlit) ---
st.title("🔐 Digital Clock Cipher (No-Z Edition)")

st.write("""
Aplikasi ini menggunakan waktu (Jam & Menit) sebagai kunci enkripsi dinamis. 
**Aturan Khusus:** Alfabet hanya terdiri dari 25 karakter (A-Y). 
Huruf **Z** otomatis diubah menjadi **Y** untuk menjaga integritas algoritma mod 25.
""")

# Input Jam dan Menit berdampingan
col1, col2 = st.columns(2)
with col1:
    h = st.number_input("Input Jam (H)", min_value=0, max_value=23, value=datetime.datetime.now().hour)
with col2:
    m = st.number_input("Input Menit (M)", min_value=0, max_value=59, value=datetime.datetime.now().minute)

# Tab Enkripsi & Dekripsi
tab_enc, tab_dec = st.tabs(["Enkripsi", "Dekripsi"])

with tab_enc:
    pesan_asli = st.text_area("Pesan Asli:", placeholder="Ketik pesan di sini (Contoh: ZEBRA)...", key="enc_input")
    if st.button("Proses Enkripsi"):
        if pesan_asli:
            hasil = process_cipher(pesan_asli, h, m, mode="Enkripsi")
            st.success(f"Hasil Enkripsi: {hasil}")
        else:
            st.warning("Silakan masukkan pesan terlebih dahulu.")

with tab_dec:
    pesan_terenkripsi = st.text_area("Pesan Terenkripsi:", placeholder="Masukkan kode rahasia...", key="dec_input")
    if st.button("Proses Dekripsi"):
        if pesan_terenkripsi:
            hasil = process_cipher(pesan_terenkripsi, h, m, mode="Dekripsi")
            st.info(f"Pesan Asli: {hasil}")
        else:
            st.warning("Silakan masukkan pesan yang ingin didekripsi.")

st.markdown("---")
st.caption("Dikembangkan dengan Python & Streamlit")
