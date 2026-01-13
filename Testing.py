import streamlit as st
import datetime
import pytz

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Digital Clock Cipher", page_icon="🔐")

# --- Fungsi Mengambil Waktu Jakarta ---
def get_current_jakarta_time():
    # Menetapkan zona waktu ke Asia/Jakarta (WIB)
    tz_jakarta = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz_jakarta)
    return now.hour, now.minute

# --- Fungsi Logika Kriptografi ---
def process_cipher(text, hour, minute, mode="Enkripsi"):
    # Alfabet tanpa huruf Z (25 karakter)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXY"
    shift = (hour + minute) % 25
    
    if mode == "Dekripsi":
        shift = -shift
        
    # Normalisasi: Kapital, spasi tetap, Z jadi Y
    text = text.upper().replace('Z', 'Y')
    result = ""
    
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
Aplikasi ini membaca waktu **Jakarta (WIB)** saat ini secara otomatis sebagai kunci enkripsi. 
**Aturan:** Huruf **Z** akan dikonversi menjadi **Y**.
""")

# Ambil waktu otomatis saat ini
current_h, current_m = get_current_jakarta_time()

# Layout Input (ReadOnly agar user tahu waktu yang terbaca otomatis)
col1, col2 = st.columns(2)
with col1:
    h = st.number_input("Jam Saat Ini (H)", value=current_h, disabled=True)
with col2:
    m = st.number_input("Menit Saat Ini (M)", value=current_m, disabled=True)

st.info(f"🕒 Terdeteksi Waktu Jakarta: **{current_h:02d}:{current_m:02d}** (Kunci Shift: {current_h + current_m})")

# Tab Enkripsi & Dekripsi
tab_enc, tab_dec = st.tabs(["Enkripsi", "Dekripsi"])

with tab_enc:
    pesan_asli = st.text_area("Pesan Asli:", placeholder="Ketik pesan di sini...", key="enc_input")
    if st.button("Proses Enkripsi", type="primary"):
        if pesan_asli:
            # Menggunakan waktu terbaru saat tombol diklik
            hasil = process_cipher(pesan_asli, current_h, current_m, mode="Enkripsi")
            st.success(f"**Hasil Enkripsi:** {hasil}")
        else:
            st.warning("Masukkan pesan terlebih dahulu.")

with tab_dec:
    pesan_terenkripsi = st.text_area("Pesan Terenkripsi:", placeholder="Tempel kode rahasia...", key="dec_input")
    if st.button("Proses Dekripsi", type="primary"):
        if pesan_terenkripsi:
            # Menggunakan waktu yang sama untuk dekripsi
            hasil = process_cipher(pesan_terenkripsi, current_h, current_m, mode="Dekripsi")
            st.
