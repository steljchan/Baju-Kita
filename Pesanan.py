import tkinter as tk
from tkinter import messagebox
import os
import ast
import Profile

posts_file = "posts.txt"
orderan_file = "orderan.txt"
user_data_file = "user_data.txt"
riwayat_file = "riwayat.txt"
user_data = {}

class pesanan(tk.Tk):
    def __init__(self, username, account_type):
        tk.Tk.__init__(self)
        self.title("Status Pesanan")
        self.geometry("600x400")
        self.configure(bg="#f4f4f4")
        self.account_type = account_type
        self.username = username
        self.ensure_file_exists()
        self.create_riwayat_file()
        self.load_user_data()
        
        self.order_listbox = tk.Listbox(self, font=("Arial", 12), width=50, height=10)
        self.order_listbox.pack(pady=10)
        
        self.load_orders()
        
        self.view_details_button = tk.Button(self, text="Lihat Detail Pesanan", font=("Arial", 12), bg="#4caf50", fg="white", command=self.view_order_details)
        self.view_details_button.pack(pady=20)
        
        self.selesai_button = tk.Button(self, text="Selesai", font=("Arial", 12), bg="#4caf50", fg="white", command=self.complete_order, state=tk.DISABLED)
        self.selesai_button.pack(pady=5)
        
        self.back_button = tk.Button(self, text="Kembali", font=("Arial", 12), bg="#4caf50", fg="white", command=self.profile)
        self.back_button.pack(pady=10)
    
    def ensure_file_exists(self):
        if not os.path.exists(posts_file):
            with open(posts_file, "w"):
                pass

    def create_riwayat_file(self):
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
            with open(orderan_file, "r") as file:
                orders = file.readlines()
                for order in orders:
                    parts = order.strip().split(',')
                    if len(parts) >= 7:
                        user = parts[0]
                        post_name = parts[1]
                        creator = parts[2]
                        price = parts[3]
                        address = parts[4]
                        delivery_method = parts[5]
                        status = parts[6]
                        post_info_str = parts[7] if len(parts) > 7 else ''  

                        if user == self.username:
                            order_display = f"Pesanan: {post_name} | Creator: {creator} | Harga: {price} | Alamat: {address} | Metode Pengiriman: {delivery_method} | Status: {status} | Post Info: {post_info_str}"
                            self.order_listbox.insert(tk.END, order_display)
        except Exception as e:
            print(f"Error reading {orderan_file}: {e}")
    
    def view_order_details(self):
        try:
            selected_index = self.order_listbox.curselection()[0]  
            order_text = self.order_listbox.get(selected_index)  
            order_parts = order_text.split('|')
            self.selected_order_id = order_parts[0].split(':')[1].strip()
            self.selected_creator = order_parts[1].split(':')[1].strip()
            price = order_parts[2].split(':')[1].strip()
            address = order_parts[3].split(':')[1].strip()
            method = order_parts[4].split(':')[1].strip()
            status = order_parts[5].split(':')[1].strip()
            
            order_details = f"Pesanan: {self.selected_order_id}\nCreator: {self.selected_creator}\nHarga: {price}\nAlamat: {address}\nPengiriman: {method}\nStatus: {status}"
            
            messagebox.showinfo("Deskripsi Pesanan", order_details)
            
            if status == "Pesanan sudah sampai":
                self.selesai_button.config(state=tk.NORMAL)
            else:
                self.selesai_button.config(state=tk.DISABLED)
            
        except IndexError:
            messagebox.showwarning("Tidak ada pesanan yang dipilih", "Tolong pilih pesanan yang ingin dilihat.")
    
    def complete_order(self):
        updated_orders = []
        order_updated = False
        completed_order = None
        try:
            with open(orderan_file, "r") as file:
                orders = file.readlines()
            for order in orders:
                parts = order.strip().split(',')
                if len(parts) >= 7 and parts[1].strip() == self.selected_order_id and parts[0].strip() == self.username:
                    parts[6] = "Pesanan sudah selesai"  
                    completed_order = ','.join(parts) 
                    order_updated = True
                else:
                    updated_orders.append(order.strip())
            if order_updated:
                with open(orderan_file, "w") as file:
                    file.writelines('\n'.join(updated_orders) + '\n')
                self.add_to_riwayat_file(self.username, completed_order)
                messagebox.showinfo("Pesanan Selesai", "Pesanan berhasil dipindahkan ke riwayat dengan status selesai.")
                self.load_orders()
            else:
                messagebox.showwarning("Pesanan Tidak Ditemukan", "Pesanan tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
    
    def add_to_riwayat_file(self, username, completed_order):
        try:
            riwayat_data = {}
            if os.path.exists(riwayat_file):
                with open(riwayat_file, "r") as file:
                    for line in file:
                        user, orders_str = line.strip().split(":", 1)
                        orders = orders_str.strip("[]").split(", ")
                        riwayat_data[user] = [order.strip() for order in orders]

            completed_order_parts = completed_order.split(',')
            post_info_str = completed_order_parts[7] if len(completed_order_parts) > 7 else '{}'
            completed_order_entry = f"{post_info_str} | Pesanan sudah selesai"

            if username not in riwayat_data:
                riwayat_data[username] = []
            riwayat_data[username].append(completed_order_entry)

            with open(riwayat_file, "w") as file:
                for user, orders in riwayat_data.items():
                    orders_str = ", ".join(orders)
                    file.write(f"{user}:[{orders_str}]\n")

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat memperbarui riwayat: {e}")
    
    def profile(self):
        self.destroy()
        Profile.profile(self.username, self.account_type).mainloop()
