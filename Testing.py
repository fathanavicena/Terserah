import streamlit as st
import datetime
import pytz

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Digital Clock Cipher", page_icon="🔐")
# 1 & 2. Import dan Setup (Sudah termasuk di atas)

def get_now():
    """Mengambil objek waktu Jakarta terbaru."""
    return datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
# 3. Buat fungsi untuk hitung luas dan keliling
# Hitung Luas
def luas_segitiga(a, t):
    return (a * t) / 2

def process_cipher(text, hour, minute, mode="Enkripsi"):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXY"
    shift = (hour + minute) % 25
    if mode == "Dekripsi":
        shift = -shift
def luas_persegi_panjang(p, l):
    return p * l

def luas_jajar_genjang(a, t):
    return a * t

# Hitung Keliling
def keliling_segitiga(a, b, c):
    return a + b + c

def keliling_persegi_panjang(p, l):
    return 2 * (p + l)

def keliling_jajar_genjang(a, b):
    return 2 * (a + b)

# 4. Masukkan setiap fungsi ke dalam dictionary sebagai opsi
hitungLuas = {
    "Luas Segitiga": {
        "Fungsi": luas_segitiga,
        "Inputan": ['Alas', 'Tinggi']
    },
    "Luas Persegi Panjang": {
        "Fungsi": luas_persegi_panjang,
        "Inputan": ['Panjang', 'Lebar']
    },
    "Luas Jajar Genjang": {
        "Fungsi": luas_jajar_genjang,
        "Inputan": ['Alas', 'Tinggi']
    }
}

hitungKeliling = {
    "Keliling Segitiga": {
        "Fungsi": keliling_segitiga,
        "Inputan": ['Sisi A', 'Sisi B', 'Sisi C']
    },
    "Keliling Persegi Panjang": {
        "Fungsi": keliling_persegi_panjang,
        "Inputan": ['Panjang', 'Lebar']
    },
    "Keliling Jajar Genjang": {
        "Fungsi": keliling_jajar_genjang,
        "Inputan": ['Sisi A', 'Sisi B']
    }
}

# 5. Buat Judul dan Select Box Utama
st.title("Aplikasi Hitung Bangun Datar")

opt = st.selectbox(
    label="Pilih operasi perhitungan",
    options=['Hitung Luas', 'Hitung Keliling']
)

# 6. Fungsi untuk melakukan opsi
def pilih_rumus(option):
    allRumus = {}
    if (option == 'Hitung Luas'):
        allRumus = hitungLuas
    else:
        allRumus = hitungKeliling
    return allRumus

# 7. Integrasi fungsi pilih_rumus dengan Radio Button
all_rumus = pilih_rumus(opt)

pilih_hitung = st.radio(
    label='Pilih Hitung',
    options=all_rumus.keys(),
    horizontal=True
)

# 8. Buat inputan fleksibel menggunakan Number Input
inputs = [st.number_input(label=label, value=0.0) for label in all_rumus[pilih_hitung]["Inputan"]]

# 9. Tombol Hitung dan Menampilkan Hasil dengan Markdown
if st.button('Hitung'):
    # Mengambil fungsi dari dictionary dan memasukkan list inputs sebagai argumen
    hasil = all_rumus[pilih_hitung]["Fungsi"](*inputs)

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
    st.markdown(f'<h2 style="color:green; text-align:center;">Hasil: {hasil}</h2>', 
                unsafe_allow_html=True)
