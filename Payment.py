import tkinter as tk
from tkinter import simpledialog, messagebox
import Homepage
import os

user_data_file = "user_data.txt"
orderan_file = "orderan.txt"
user_data = {}

class selesai(tk.Tk):
    def __init__(self, username, account_type):
        tk.Tk.__init__(self)
        self.title("Pembayaran")
        self.geometry("500x400") 
        self.configure(bg="#f4f4f4")
        self.ensure_file_exists()
        self.load_user_data()
        self.username = username
        self.account_type = account_type
        if username not in user_data:
            user_data[username] = {
                'basket': [],
                'donasi': [],
                'basket_count': 0,
                'donasi_count': 0,
                "kelamin": "",
                'organisasi': "",
                'No. Tlp': "",
                "email": "",
                'alamat': []  
            }
        self.user_info = user_data[username]
        
        self.selesai_button = tk.Button(self, text="Bayar", font=("Arial", 12), bg="#4caf50", fg="white", command=self.selesai)
        self.selesai_button.pack(pady=10)
        
        self.cancel_button = tk.Button(self, text="Batal", font=("Arial", 12), bg="#4caf50", fg="white", command=self.homepage)
        self.cancel_button.pack(pady=10)
    
    def ensure_file_exists(self):
        if not os.path.exists(orderan_file):
            open(orderan_file, "w").close()
    
    def load_user_data(self):
        global user_data
        if os.path.exists(user_data_file):
            with open(user_data_file, "r") as file:
                for line in file:
                    try:
                        parts = line.strip().split(',')
                        if len(parts) < 6:
                            continue  
                        username = parts[0]
                        basket_count = int(parts[1])
                        donasi_count = int(parts[2])
                        kelamin = parts[3]
                        organisasi = parts[4]
                        tlp = parts[5]
                        email = parts[6]
                        alamat = parts[7].split(';') if len(parts) > 7 and parts[7] else [] 
                        
                        user_data[username] = {
                            'basket': [],
                            'donasi': [],
                            'basket_count': basket_count,
                            'donasi_count': donasi_count,
                            'kelamin': kelamin,
                            'organisasi': organisasi,
                            'No. Tlp': tlp,
                            'email': email,
                            'alamat': alamat
                        }
                    except Exception as e:
                        print(f"Error processing line: {line}. Error: {e}")
    
    def selesai(self):
        try:
            with open(orderan_file, "r") as file:
                lines = file.readlines()
            updated = False  
            with open(orderan_file, "w") as file:
                for line in lines:
                    parts = line.strip().split(",")
                    if len(parts) > 6 and parts[0] == self.username and parts[6] == "belum dibayar":
                        parts[6] = "sudah dibayar" 
                        updated = True
                    file.write(",".join(parts) + "\n")
            if updated:
                messagebox.showinfo("Sukses", "Pembayaran berhasil! Status pesanan diubah ke 'sudah dibayar'.")
                self.destroy()  
                Homepage.Homepage(self.username, self.account_type).mainloop()
            else:
                messagebox.showwarning("Peringatan", "Tidak ada pesanan yang statusnya 'belum dibayar'.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui status pembayaran: {e}")
    
    def homepage(self):
        self.destroy()
        Homepage.Homepage(self.username, self.account_type).mainloop()