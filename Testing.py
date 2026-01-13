import datetime
import string

def get_time_elements():
    """Mengambil jam dan menit saat ini."""
    now = datetime.datetime.now()
    return now.hour, now.minute

def generate_alphabet_no_z():
    """Menghasilkan daftar alfabet tanpa huruf 'Z'."""
    # Menghasilkan 'ABC...XY' (Z dihapus)
    return string.ascii_uppercase.replace('Z', '')

def encrypt(text, hour, minute):
    """
    Algoritma enkripsi:
    1. Menggunakan (jam + menit) sebagai nilai pergeseran (shift).
    2. Hanya mengenkripsi huruf yang ada di alfabet (A-Y).
    3. Melewati huruf 'Z'.
    """
    alphabet = generate_alphabet_no_z()
    shift = (hour + minute) % len(alphabet)
    result = ""
    
    # Ubah teks ke uppercase untuk konsistensi
    text = text.upper()
    
    for char in text:
        if char == 'Z':
            # Jika huruf adalah Z, biarkan tetap Z (sesuai instruksi)
            result += char
        elif char in alphabet:
            # Cari posisi baru dengan pergeseran
            idx = alphabet.find(char)
            new_idx = (idx + shift) % len(alphabet)
            result += alphabet[new_idx]
        else:
            # Karakter non-alfabet (spasi, angka) tetap sama
            result += char
            
    return result, shift

# --- Main Execution ---
if __name__ == "__main__":
    h, m = get_time_elements()
    pesan = "HALO DUNIA DARI GEMINI"
    
    encrypted_text, shift_used = encrypt(pesan, h, m)
    
    print(f"--- Log Enkripsi ---")
    print(f"Waktu Sistem : {h:02d}:{m:02d}")
    print(f"Nilai Shift  : {shift_used} (Jam + Menit)")
    print(f"Pesan Asli   : {pesan}")
    print(f"Hasil Enkripsi: {encrypted_text}")
