import tkinter as tk
from tkinter import messagebox

class TimeShiftCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Clock Cipher (No-Z)")
        self.root.geometry("400x450")

        # Alfabet tanpa huruf 'Z'
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXY"

        # UI Elements
        tk.Label(root, text="Digital Clock Cipher", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(root, text="Masukkan Pesan:").pack()
        self.entry_message = tk.Entry(root, width=40)
        self.entry_message.pack(pady=5)

        tk.Label(root, text="Jam (00-23):").pack()
        self.entry_hour = tk.Entry(root, width=10)
        self.entry_hour.pack(pady=5)

        tk.Label(root, text="Menit (00-59):").pack()
        self.entry_minute = tk.Entry(root, width=10)
        self.entry_minute.pack(pady=5)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Enkripsi", command=self.encrypt_message, bg="lightgreen").pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Dekripsi", command=self.decrypt_message, bg="lightcyan").pack(side=tk.LEFT, padx=10)

        tk.Label(root, text="Hasil:").pack()
        self.result_text = tk.Text(root, height=5, width=40)
        self.result_text.pack(pady=5)

    def get_key(self):
        try:
            h = int(self.entry_hour.get())
            m = int(self.entry_minute.get())
            return (h + m) % 25
        except ValueError:
            messagebox.showerror("Error", "Masukkan jam dan menit dalam angka!")
            return None

    def process_text(self, text, key, mode="encrypt"):
        text = text.upper().replace("Z", "A") # Ganti Z dengan A sesuai aturan No-Z
        result = ""
        
        for char in text:
            if char in self.alphabet:
                idx = self.alphabet.find(char)
                if mode == "encrypt":
                    new_idx = (idx + key) % 25
                else:
                    new_idx = (idx - key) % 25
                result += self.alphabet[new_idx]
            else:
                result += char # Tetap biarkan spasi atau simbol
        return result

    def encrypt_message(self):
        key = self.get_key()
        if key is not None:
            msg = self.entry_message.get()
            encrypted = self.process_text(msg, key, "encrypt")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"{encrypted}-{self.entry_hour.get()}{self.entry_minute.get()}")

    def decrypt_message(self):
        key = self.get_key()
        if key is not None:
            msg = self.entry_message.get()
            # Jika input mengandung tanda hubung (seperti NCP-1141), ambil bagian depannya saja
            if "-" in msg:
                msg = msg.split("-")[0]
            decrypted = self.process_text(msg, key, "decrypt")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, decrypted)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeShiftCipherApp(root)
    root.mainloop()
