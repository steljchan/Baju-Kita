import tkinter as tk
from tkinter import messagebox
import os
import ast
import Profile

riwayat_file = "riwayat.txt"
user_data_file = "user_data.txt"
user_data = {}

class riwayat(tk.Toplevel):
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
                        # Parse the list of orders
                        orders_list = orders_str.strip("[]").split(", ")
                        # Ensure there are at most 5 orders (queue behavior)
                        while len(orders_list) > 5:
                            orders_list.pop(0)

                        for order_str in orders_list:
                            try:
                                # Clean up the format: replace semicolons with commas and single quotes with double quotes
                                order_str = order_str.replace("'", '"').replace(";", ",")
                                self.order_listbox.insert(tk.END, order_str)
                            except Exception as e:
                                print(f"Error parsing order: {order_str} -> {e}")
                    
                        # Update the file with the limited list of orders
                        self.update_riwayat_file(user, orders_list)
        except Exception as e:
            print(f"Error reading {riwayat_file}: {e}")
    
    def update_riwayat_file(self, username, updated_orders):
        try:
            riwayat_data = {}
            if os.path.exists(riwayat_file):
                with open(riwayat_file, "r") as file:
                    for line in file:
                        user, orders_str = line.strip().split(":", 1)
                        riwayat_data[user] = orders_str.strip("[]").split(", ")
            # Update only the current user's orders
            riwayat_data[username] = updated_orders
            with open(riwayat_file, "w") as file:
                for user, orders in riwayat_data.items():
                    orders_str = ", ".join(orders)
                    file.write(f"{user}:[{orders_str}]\n")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat memperbarui riwayat: {e}")
    
    def back(self):
        self.destroy()
        Profile.profile(self.username, self.account_type).mainloop()
