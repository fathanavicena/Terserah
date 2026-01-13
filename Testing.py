import streamlit as st
import datetime
import pytz

# --- 1. LOGIKA KRIPTOGRAFI ---
def process_cipher(text, hour, minute, mode="Enkripsi"):
    # Alfabet tanpa huruf Z (Total 25 karakter: A-Y)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXY"
    shift = (hour + minute) % 25
    
    if mode == "Dekripsi":
        shift = -shift
        
    # Aturan Baru: Huruf Z diganti menjadi Y sebelum diproses
    text = text.upper().replace('Z', 'Y')
    
    result = ""
    for char in text:
        if char in alphabet:
            idx = alphabet.find(char)
            new_idx = (idx + shift) % 25
            result += alphabet[new_idx]
        else:
            # Karakter selain huruf (spasi, angka, simbol) tetap dipertahankan
            result += char
            
    return result

# --- 2. TAMPILAN SIDEBAR ---
st.sidebar.title("⚙️ Pengaturan")
mode_waktu = st.sidebar.radio(
    "Pilih Mode Input Waktu:",
    ("Otomatis (Jakarta)", "Manual")
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Aturan Logika Terbaru:**
1. Kunci = Jam + Menit.
2. Huruf **Z** otomatis diubah menjadi **Y**.
3. Alfabet: A-Y (25 karakter).
""")

# --- 3. LOGIKA PENGAMBILAN WAKTU ---
if mode_waktu == "Otomatis (Jakarta)":
    tz_jakarta = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz_jakarta)
    h_val, m_val = now.hour, now.minute
else:
    col_h, col_m = st.columns(2)
    with col_h:
        h_val = st.number_input("Input Jam (H)", 0, 23, 12)
    with col_m:
        m_val = st.number_input("Input Menit (M)", 0, 59, 0)

# --- 4. TAMPILAN UTAMA ---
st.title("🔐 Digital Clock Cipher (No-Z Edition)")

# Tampilan Metrik Jam Aktif
c1, c2 = st.columns(2)
c1.metric("Jam Digunakan", f"{h_val:02d}")
c2.metric("Menit Digunakan", f"{m_val:02d}")

tab_enc, tab_dec = st.tabs(["Enkripsi", "Dekripsi"])

with tab_enc:
    pesan_asli = st.text_area("Pesan Asli:", placeholder="Ketik pesan... (Z akan menjadi Y)")
    if st.button("Jalankan Enkripsi", type="primary"):
        if pesan_asli:
            # Refresh waktu jika otomatis agar sangat akurat saat klik
            if mode_waktu == "Otomatis (Jakarta)":
                now_refresh = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
                h_val, m_val = now_refresh.hour, now_refresh.minute
            
            hasil = process_cipher(pesan_asli, h_val, m_val, mode="Enkripsi")
            st.success(f"**Hasil Enkripsi:** {hasil}")
            st.caption(f"Log: Kunci {h_val:02d}:{m_val:02d} (Shift: {h_val+m_val})")

with tab_dec:
    pesan_kode = st.text_area("Pesan Terenkripsi:", placeholder="Tempel kode di sini...")
    if st.button("Jalankan Dekripsi", type="primary"):
        if pesan_kode:
            # Menggunakan jam yang sama untuk dekripsi
            hasil = process_cipher(pesan_kode, h_val, m_val, mode="Dekripsi")
            st.info(f"**Hasil Dekripsi:** {hasil}")

st.markdown("---")
st.caption("Aplikasi Kriptografi Berbasis Waktu Jakarta")
