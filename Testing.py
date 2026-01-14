import streamlit as st
import datetime
import pytz

# --- 1. LOGIKA KRIPTOGRAFI ---
def process_cipher(text, hour, minute, mode="Enkripsi"):
    # Alfabet tanpa huruf Z (25 karakter: A-Y)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXY"
    shift = (hour + minute) % 25
    
    if mode == "Dekripsi":
        shift = -shift
        
    # PERUBAHAN DI SINI: Huruf Z diganti menjadi Y (bukan dihapus)
    # Ini memastikan jumlah karakter tetap dan bisa didekripsi dengan benar
    text = text.upper().replace('Z', 'Y')
    
    result = ""
    for char in text:
        if char in alphabet:
            idx = alphabet.find(char)
            new_idx = (idx + shift) % 25
            result += alphabet[new_idx]
        else:
            result += char # Spasi, angka, dan simbol tetap
    return result

# --- 2. TAMPILAN SIDEBAR ---
st.sidebar.title("⚙️ Menu Pilihan")
mode_waktu = st.sidebar.radio(
    "Pilih Mode Waktu:",
    ("Otomatis (Jakarta)", "Manual")
)

st.sidebar.markdown("---")
# Update pesan peringatan di sidebar
st.sidebar.info("ℹ️ Huruf **Z** akan otomatis dikonversi menjadi **Y** agar pesan tetap sinkron saat didekripsi.")

# --- 3. LOGIKA WAKTU ---
if mode_waktu == "Otomatis (Jakarta)":
    tz_jkt = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz_jkt)
    h_val = now.hour
    m_val = now.minute
else:
    # Mode manual menampilkan input di kolom utama atau sidebar
    h_val = st.sidebar.number_input("Input Jam (H)", 0, 23, 9)
    m_val = st.sidebar.number_input("Input Menit (M)", 0, 59, 30)

# --- 4. TAMPILAN UTAMA ---
st.title("🔐 Digital Clock Cipher (No-Z Edition)")

# Tampilkan jam yang sedang aktif
st.info(f"🕒 Waktu Aktif: **{h_val:02d}:{m_val:02d}** (Kunci Shift: {h_val + m_val})")

tab_enc, tab_dec = st.tabs(["Enkripsi", "Dekripsi"])

with tab_enc:
    pesan_asli = st.text_area("Pesan Asli:", placeholder="Ketik pesan di sini... (Contoh: ZEBRA akan diproses sebagai YEBRA)")
    if st.button("Proses Enkripsi", type="primary"):
        if pesan_asli:
            # Update waktu real-time jika mode otomatis
            if mode_waktu == "Otomatis (Jakarta)":
                now_curr = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
                h_val, m_val = now_curr.hour, now_curr.minute
            
            hasil = process_cipher(pesan_asli, h_val, m_val, "Enkripsi")
            st.success(f"**Hasil Enkripsi:** {hasil}")
        else:
            st.error("Isi pesan terlebih dahulu!")

with tab_dec:
    pesan_kode = st.text_area("Pesan Terenkripsi:", placeholder="Tempel kode rahasia di sini...")
    if st.button("Proses Dekripsi"):
        if pesan_kode:
            # Menggunakan waktu yang sama dengan saat enkripsi
            hasil = process_cipher(pesan_kode, h_val, m_val, "Dekripsi")
            st.info(f"**Pesan Asli (Z menjadi Y):** {hasil}")
        else:
            st.error("Isi kode rahasia!")

st.markdown("---")
st.caption("Dikembangkan dengan Streamlit | Logika: Modulo 25 (A-Y)")
