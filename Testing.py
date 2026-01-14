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
        
    # Aturan: Huruf Z diganti menjadi Y agar pesan tetap utuh
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
st.sidebar.info("ℹ️ Huruf **Z** otomatis dikonversi menjadi **Y**.")

# --- 3. LOGIKA PENGAMBILAN WAKTU ---
# Mengambil waktu awal untuk tampilan info di atas
tz_jkt = pytz.timezone('Asia/Jakarta')
now_init = datetime.datetime.now(tz_jkt)

if mode_waktu == "Otomatis (Jakarta)":
    h_val = now_init.hour
    m_val = now_init.minute
else:
    h_val = st.sidebar.number_input("Input Jam (H)", 0, 23, now_init.hour)
    m_val = st.sidebar.number_input("Input Menit (M)", 0, 59, now_init.minute)

# --- 4. TAMPILAN UTAMA ---
st.title("🔐 Digital Clock Cipher (No-Z Edition)")

# Box informasi waktu aktif (sebelum diproses)
st.info(f"🕒 Waktu Sistem Saat Ini: **{h_val:02d}:{m_val:02d}**")

tab_enc, tab_dec = st.tabs(["Enkripsi", "Dekripsi"])

with tab_enc:
    pesan_asli = st.text_area("Pesan Asli:", placeholder="Ketik pesan di sini...")
    if st.button("Proses Enkripsi", type="primary"):
        if pesan_asli:
            # Jika otomatis, ambil waktu presisi saat tombol diklik
            if mode_waktu == "Otomatis (Jakarta)":
                now_curr = datetime.datetime.now(tz_jkt)
                h_val, m_val = now_curr.hour, now_curr.minute
            
            hasil = process_cipher(pesan_asli, h_val, m_val, "Enkripsi")
            
            # Menampilkan hasil enkripsi
            st.success(f"**Hasil Enkripsi:** {hasil}")
            
            # MENAMPILKAN WAKTU DI AKHIR SETELAH ENKRIPSI (Sesuai Permintaan)
            st.markdown(f"""
            <div style="background-color: #262730; padding: 10px; border-radius: 5px; border-left: 5px solid #ff4b4b;">
                ✅ <b>Enkripsi Berhasil!</b><br>
                🕒 Waktu yang digunakan: <b>{h_val:02d}:{m_val:02d} WIB</b><br>
                🔑 Kunci Shift: <b>{h_val + m_val}</b>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Isi pesan terlebih dahulu!")

with tab_dec:
    pesan_kode = st.text_area("Pesan Terenkripsi:", placeholder="Tempel kode di sini...")
    if st.button("Proses Dekripsi"):
        if pesan_kode:
            # Gunakan waktu yang tertera pada input/sistem
            hasil = process_cipher(pesan_kode, h_val, m_val, "Dekripsi")
            st.info(f"**Hasil Dekripsi:** {hasil}")
            st.caption(f"Menggunakan referensi waktu: {h_val:02d}:{m_val:02d}")
        else:
            st.error("Isi kode rahasia!")

st.markdown("---")
st.caption("Dikembangkan dengan Streamlit | Logika: Modulo 25 (A-Y)")
