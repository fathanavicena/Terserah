import streamlit as st
import datetime
import pytz

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Digital Clock Cipher", page_icon="🔐")

def get_now():
    """Mengambil objek waktu Jakarta terbaru."""
    return datetime.datetime.now(pytz.timezone('Asia/Jakarta'))

def process_cipher(text, hour, minute, mode="Enkripsi"):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXY"
    shift = (hour + minute) % 25
    if mode == "Dekripsi":
        shift = -shift
    
    # Aturan: Huruf Z menjadi Y
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

# Mengambil waktu saat ini untuk tampilan awal
now = get_now()

st.write(f"Aplikasi ini menggunakan waktu **Jakarta (WIB)** secara otomatis.")

# Menampilkan jam yang terbaca saat ini di UI
col1, col2 = st.columns(2)
with col1:
    st.metric("Jam (H)", f"{now.hour:02d}")
with col2:
    st.metric("Menit (M)", f"{now.minute:02d}")

tab_enc, tab_dec = st.tabs(["Enkripsi", "Dekripsi"])

with tab_enc:
    pesan_asli = st.text_area("Pesan Asli:", placeholder="Ketik pesan...", key="enc_input")
    if st.button("Proses Enkripsi", type="primary"):
        # MENGAMBIL WAKTU TERBARU SAAT TOMBOL DIKLIK
        current_now = get_now()
        h, m = current_now.hour, current_now.minute
        
        if pesan_asli:
            hasil = process_cipher(pesan_asli, h, m, mode="Enkripsi")
            st.success(f"**Hasil Enkripsi:** {hasil}")
            st.caption(f"Digunakan waktu: {h:02d}:{m:02d} (Shift: {h+m})")

with tab_dec:
    pesan_terenkripsi = st.text_area("Pesan Terenkripsi:", placeholder="Tempel kode...", key="dec_input")
    if st.button("Proses Dekripsi", type="primary"):
        # MENGAMBIL WAKTU TERBARU SAAT TOMBOL DIKLIK
        current_now = get_now()
        h, m = current_now.hour, current_now.minute
        
        if pesan_terenkripsi:
            hasil = process_cipher(pesan_terenkripsi, h, m, mode="Dekripsi")
            st.info(f"**Hasil Dekripsi:** {hasil}")
            st.caption(f"Digunakan waktu: {h:02d}:{m:02d} (Shift: {h+m})")

st.markdown("---")
if st.button("🔄 Refresh Waktu"):
    st.rerun() # Memaksa aplikasi membaca ulang waktu Jakarta
