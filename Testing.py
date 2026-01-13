import streamlit as st
import datetime
import pytz  # Library untuk mengatur zona waktu

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Digital Clock Cipher", page_icon="🔐")

# --- Logika Waktu Jakarta ---
def get_jakarta_time():
    tz_jakarta = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz_jakarta)
    return now.hour, now.minute

# --- Fungsi Cipher ---
def process_cipher(text, hour, minute, mode="Enkripsi"):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXY"
    shift = (hour + minute) % 25
    
    if mode == "Dekripsi":
        shift = -shift
        
    result = ""
    text = text.upper().replace('Z', 'Y')
    
    for char in text:
        if char in alphabet:
            idx = alphabet.find(char)
            new_idx = (idx + shift) % 25
            result += alphabet[new_idx]
        else:
            result += char
            
    return result

# --- Tampilan UI ---
st.title("🔐 Digital Clock Cipher (No-Z Edition)")

st.write("""
Aplikasi ini menggunakan waktu **Jakarta (WIB)** saat ini sebagai kunci enkripsi dinamis.
""")

# Mengambil waktu Jakarta secara otomatis
auto_h, auto_m = get_jakarta_time()

# Input Jam dan Menit (Otomatis terisi namun tetap bisa diubah manual jika perlu)
col1, col2 = st.columns(2)
with col1:
    h = st.number_input("Input Jam (H)", min_value=0, max_value=23, value=auto_h)
with col2:
    m = st.number_input("Input Menit (M)", min_value=0, max_value=59, value=auto_m)

st.info(f"🕒 Waktu Jakarta saat ini: **{auto_h:02d}:{auto_m:02d}** (Kunci: {h+m})")

# Tab Enkripsi & Dekripsi
tab_enc, tab_dec = st.tabs(["Enkripsi", "Dekripsi"])

with tab_enc:
    pesan_asli = st.text_area("Pesan Asli:", placeholder="Ketik pesan di sini...", key="enc_input")
    if st.button("Proses Enkripsi"):
        if pesan_asli:
            hasil = process_cipher(pesan_asli, h, m, mode="Enkripsi")
            st.success(f"Hasil Enkripsi: {hasil}")

with tab_dec:
    pesan_terenkripsi = st.text_area("Pesan Terenkripsi:", placeholder="Masukkan kode rahasia...", key="dec_input")
    if st.button("Proses Dekripsi"):
        if pesan_terenkripsi:
            hasil = process_cipher(pesan_terenkripsi, h, m, mode="Dekripsi")
            st.info(f"Pesan Asli: {hasil}")

st.markdown("---")
st.caption("Dikembangkan dengan Python & Streamlit | Zona Waktu: Asia/Jakarta")
