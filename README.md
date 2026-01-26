# Digital Clock Cipher: Dynamic Symbol Edition

Algoritma ini adalah sistem kriptografi pergeseran waktu yang menggunakan **Dinamika Karakter ke-26**.

## Fitur Unggulan
1. **Dynamic Z-Substitution**: Berbeda dengan cipher standar, huruf 'Z' tidak hilang, melainkan menyamar menjadi 24 simbol berbeda tergantung pada jam eksekusi ($H$).
2. **Time-Based Key**: Kunci pergeseran ($K$) dihitung menggunakan jam dan menit:
   $$K = (H + M) \pmod{25}$$
3. **Z-Symbol Table**:
   - Jam 00: `!`
   - Jam 01: `@`
   - ... (dan seterusnya hingga 24 simbol unik)

## Cara Kerja
Jika Anda mengenkripsi kata "ZOO" pada jam 01:00, algoritma akan:
1. Mengubah "Z" menjadi "@".
2. Menggeser "O" berdasarkan kunci jam 01.
3. Saat dekripsi pada jam yang sama, "@" akan dikenali kembali sebagai "Z".
