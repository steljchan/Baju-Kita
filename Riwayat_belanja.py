import tkinter as tk
from tkinter import messagebox
import os
import json
import Profile

riwayat_file = "riwayat.txt"
user_data_file = "user_data.txt"
user_data = {}

class order(tk.Toplevel):
    def __init__(self, username, account_type):
        super().__init__()
        self.title("Riwayat Pesanan")
        self.geometry("500x400")
        self.configure(bg="#f4f4f4")
        self.username = username
        self.account_type = account_type
        self.ensure_file_exists()
        self.load_user_data()
        
        self.order_listbox = tk.Listbox(self, font=("Arial", 12), width=50, height=10)
        self.order_listbox.pack(pady=10)
        
        self.load_orders()
        
        self.back_button = tk.Button(self, text="Kembali", font=("Arial", 12), bg="#4caf50", fg="white", command=self.back)
        self.back_button.pack(pady=10)
    
    def ensure_file_exists(self):
        if not os.path.exists(riwayat_file):
            with open(riwayat_file, "w"):
                pass
    
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
    
    def load_orders(self):
        self.order_listbox.delete(0, tk.END)
        try:
            with open(riwayat_file, "r") as file:
                riwayat_data = file.readlines()
                for line in riwayat_data:
                    user, orders_str = line.strip().split(":", 1)
                    if user == self.username:
                        orders = json.loads(orders_str.strip())
                        for order in orders:
                            post_info = order[0] 
                            status = order[1]     
                            post_name = post_info.get('nama', 'Unknown')
                            post_status = status
                            self.order_listbox.insert(tk.END, f"{post_name} - Status: {post_status}")
                            if len(orders) > 5:
                                orders.pop(0)
                                self.update_riwayat_file(user, orders)
        except Exception as e:
            print(f"Error reading {riwayat_file}: {e}")
    
    def update_riwayat_file(self, username, updated_orders):
        try:
            riwayat_data = {}
            if os.path.exists(riwayat_file):
                with open(riwayat_file, "r") as file:
                    for line in file:
                        user, orders_str = line.strip().split(":", 1)
                        riwayat_data[user] = json.loads(orders_str.strip())
            riwayat_data[username] = updated_orders  
            with open(riwayat_file, "w") as file:
                for user, orders in riwayat_data.items():
                    file.write(f"{user}:{json.dumps(orders)}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat memperbarui riwayat: {e}")
    
    def back(self):
        self.destroy()
        Profile.profile(self.username, self.account_type).mainloop()
