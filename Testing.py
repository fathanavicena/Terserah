import streamlit as st
import datetime
import pytz

# --- 1. LOGIKA KRIPTOGRAFI ---
def process_cipher(text, hour, minute, mode="Enkripsi"):
    # Alfabet tanpa huruf Z (25 karakter)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXY"
    shift = (hour + minute) % 25
    
    if mode == "Dekripsi":
        shift = -shift
        
    # Hapus huruf Z dari teks sesuai permintaan
    text = text.upper().replace('Z', '')
    
    result = ""
    for char in text:
        if char in alphabet:
            idx = alphabet.find(char)
            new_idx = (idx + shift) % 25
            result += alphabet[new_idx]
        else:
            result += char # Spasi dan angka tetap
    return result # Ini harus di dalam fungsi (sejajar dengan for)

# --- 2. TAMPILAN SIDEBAR ---
st.sidebar.title("⚙️ Menu Pilihan")
mode_waktu = st.sidebar.radio(
    "Pilih Mode Waktu:",
    ("Otomatis (Jakarta)", "Manual")
)

st.sidebar.markdown("---")
st.sidebar.warning("⚠️ Huruf **Z** akan otomatis dihapus dari pesan.")

# --- 3. LOGIKA WAKTU ---
if mode_waktu == "Otomatis (Jakarta)":
    tz_jkt = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz_jkt)
    h_val = now.hour
    m_val = now.minute
else:
    col_h, col_m = st.columns(2)
    with col_h:
        h_val = st.number_input("Input Jam (H)", 0, 23, 9)
    with col_m:
        m_val = st.number_input("Input Menit (M)", 0, 59, 30)

# --- 4. TAMPILAN UTAMA ---
st.title("🔐 Digital Clock Cipher (No-Z Edition)")

# Tampilkan jam yang sedang aktif
st.info(f"🕒 Waktu Aktif: **{h_val:02d}:{m_val:02d}**")

tab_enc, tab_dec = st.tabs(["Enkripsi", "Dekripsi"])

with tab_enc:
    pesan_asli = st.text_area("Pesan Asli:", placeholder="Ketik di sini...")
    if st.button("Proses Enkripsi", type="primary"):
        if pesan_asli:
            # Update waktu jika otomatis klik
            if mode_waktu == "Otomatis (Jakarta)":
                now = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
                h_val, m_val = now.hour, now.minute
            
            hasil = process_cipher(pesan_asli, h_val, m_val, "Enkripsi")
            st.success(f"Hasil: {hasil}")
        else:
            st.error("Isi pesan dulu!")

with tab_dec:
    pesan_kode = st.text_area("Pesan Terenkripsi:", placeholder="Tempel kode...")
    if st.button("Proses Dekripsi"):
        if pesan_kode:
            hasil = process_cipher(pesan_kode, h_val, m_val, "Dekripsi")
            st.info(f"Pesan Asli: {hasil}")

st.markdown("---")
st.caption("Dikembangkan dengan Streamlit")
