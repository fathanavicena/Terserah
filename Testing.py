import streamlit as st
import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Time Encryptor", page_icon="🔐")

# --- FUNGSI LOGIKA ---
def encrypt_time(hours: int, minutes: int, key: int) -> tuple:
    """Mengenkripsi jam dan menit menggunakan pergeseran sederhana."""
    encrypted_hours = (hours + key) % 24
    encrypted_minutes = (minutes + key) % 60
    return encrypted_hours, encrypted_minutes

def decrypt_time(encrypted_hours: int, encrypted_minutes: int, key: int) -> tuple:
    """Mengembalikan jam dan menit ke waktu aslinya."""
    decrypted_hours = (encrypted_hours - key) % 24
    decrypted_minutes = (encrypted_minutes - key) % 60
    return decrypted_hours, decrypted_minutes

# --- UI STREAMLIT ---
st.title("🔐 Time Encryption App")
st.write("Aplikasi sederhana untuk mengenkripsi waktu menggunakan algoritma pergeseran (*Caesar-style shift*).")

# Sidebar untuk Pengaturan
st.sidebar.header("⚙️ Pengaturan")
encryption_key = st.sidebar.slider("Pilih Kunci Enkripsi (Key)", 1, 60, 15)

use_custom_time = st.sidebar.checkbox("Gunakan Waktu Kustom?")

if use_custom_time:
    col_input1, col_input2 = st.sidebar.columns(2)
    h_input = col_input1.number_input("Jam", 0, 23, 12)
    m_input = col_input2.number_input("Menit", 0, 59, 30)
else:
    now = datetime.datetime.now()
    h_input, m_input = now.hour, now.minute

# --- EKSEKUSI ---
enc_h, enc_m = encrypt_time(h_input, m_input, encryption_key)
dec_h, dec_m = decrypt_time(enc_h, enc_m, encryption_key)

# --- TAMPILAN HASIL ---
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🕒 Waktu Asli")
    st.info(f"### {h_input:02d}:{m_input:02d}")

with col2:
    st.subheader("🔐 Terenkripsi")
    st.error(f"### {enc_h:02d}:{enc_m:02d}")

with col3:
    st.subheader("🔓 Terdekripsi")
    st.success(f"### {dec_h:02d}:{dec_m:02d}")

# Penjelasan Teknis Singkat
with st.expander("Lihat Cara Kerja (Matematika)"):
    st.write("Algoritma ini menggunakan **Aritmatika Modulo**:")
    st.latex(r"Jam_{enc} = (Jam_{asli} + Key) \pmod{24}")
    st.latex(r"Menit_{enc} = (Menit_{asli} + Key) \pmod{60}")
