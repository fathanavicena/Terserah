import streamlit as st

# 1 & 2. Import dan Setup (Sudah termasuk di atas)

# 3. Buat fungsi untuk hitung luas dan keliling
# Hitung Luas
def luas_segitiga(a, t):
    return (a * t) / 2

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
    
    st.markdown(f'<h2 style="color:green; text-align:center;">Hasil: {hasil}</h2>', 
                unsafe_allow_html=True)
