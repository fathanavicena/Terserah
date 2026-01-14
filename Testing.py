import streamlit as st
import datetime
import pytz

# --- 1. LOGIKA KRIPTOGRAFI ---
def process_cipher(text, hour, minute, mode="Enkripsi"):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXY" # 25 Karakter
    shift = (hour + minute) % 25
    
    if mode == "Dekripsi":
        shift = -shift
    
    result = ""
    text = text.upper()

    if mode == "Enkripsi":
        # Mengubah Z menjadi simbol sementara agar tidak tercampur dengan alfabet A-Y
        text = text.replace('Z', '#') 
        
        for char in text:
            if char in alphabet:
                idx = alphabet.find(char)
                new_idx = (idx + shift) % 25
                result += alphabet[new_idx]
            elif char == '#':
                # Z tetap di posisi yang sama tapi ditandai
                result += '#' 
            else:
                result += char
    
    else: # MODE DEKRIPSI
        for char in text:
            if char in alphabet:
                idx = alphabet.find(char)
                new_idx = (idx + shift) % 25
                result += alphabet[new_idx]
            elif char == '#':
                # Mengembalikan simbol # menjadi Z
                result += 'Z'
            else:
                result += char
                
    return result, abs(shift)

# --- 2. SIDEBAR ---
st.sidebar.title("⚙️ Menu Pilihan")
mode_waktu = st.sidebar.radio("Pilih Mode Waktu:", ("Otomatis (Jakarta)", "Manual"))
st.sidebar.markdown("---")
st.sidebar.info("ℹ️ **Z-Support**: Huruf Z akan tetap muncul setelah dekripsi.")

# --- 3. WAKTU JAKARTA ---
tz_jkt = pytz.timezone('Asia/Jakarta')
now_init = datetime.datetime.now(tz_jkt)
h_val, m_val = now_init.hour, now_init.minute

# --- 4. TAMPILAN UTAMA ---
st.title("🔐 Digital Clock Cipher (No-Z Logic)")

if mode_waktu == "Manual":
    col_h, col_m = st.columns(2)
    with col_h:
        h_val = st.number_input("Input Jam (H)", 0, 23, now_init.hour)
    with col_m:
        m_val = st.number_input("Input Menit (M)", 0, 59, now_init.minute)

tab_enc, tab_dec = st.tabs(["Enkripsi", "Dekripsi"])

with tab_enc:
    pesan_asli = st.text_area("Pesan Asli:", placeholder="Ketik pesan...")
    if st.button("Proses Enkripsi", type="primary"):
        if pesan_asli:
            if mode_waktu == "Otomatis (Jakarta)":
                now_curr = datetime.datetime.now(tz_jkt)
                h_val, m_val = now_curr.hour, now_curr.minute
            
            hasil, shift_f = process_cipher(pesan_asli, h_val, m_val, "Enkripsi")
            st.success(f"**Hasil Enkripsi:** {hasil}")
            
            st.markdown(f"""
            <div style="background-color: #262730; padding: 15px; border-radius: 5px; border-left: 5px solid #ff4b4b; margin-top: 20px;">
                ✅ <b>Enkripsi Berhasil!</b><br>
                🕒 Waktu: <b>{h_val:02d}:{m_val:02d} WIB</b><br>
                🔑 Key Shift (Mod 25): <b>{shift_f}</b>
            </div>
            """, unsafe_allow_html=True)

with tab_dec:
    pesan_kode = st.text_area("Pesan Terenkripsi:", placeholder="Tempel kode...")
    if st.button("Proses Dekripsi"):
        if pesan_kode:
            hasil, shift_f = process_cipher(pesan_kode, h_val, m_val, "Dekripsi")
            st.info(f"**Hasil Dekripsi:** {hasil}")

st.markdown("---")
st.caption("Dikembangkan dengan Streamlit")
