import tkinter as tk
from tkinter import messagebox
import Profile
import os

user_data_file = "user_data.txt"
posts_file = "posts.txt"
orderan_file = "orderan.txt"
riwayat_file = "riwayat.txt"
user_data = {}

class order(tk.Toplevel):
    def __init__(self, username, account_type):
        super().__init__()
        self.title("Orderan")
        self.geometry("500x400")
        self.configure(bg="#f4f4f4")
        self.ensure_file_exists()
        self.load_user_data()
        self.username = username
        self.account_type = account_type
        global user_data
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
        self.order_listbox = tk.Listbox(self, font=("Arial", 12), width=50, height=10)
        self.order_listbox.pack(pady=10)
        
        self.load_orders()
        
        self.change_status_button = tk.Button(self, text="Ubah Status", font=("Arial", 12), bg="#4caf50", fg="white", command=self.change_status)
        self.change_status_button.pack(pady=20)
        
        self.back_button = tk.Button(self, text="Kembali", font=("Arial", 12), bg="#4caf50", fg="white", command=self.profile)
        self.back_button.pack(pady=10)
    
    def ensure_file_exists(self):
        for file in [orderan_file, posts_file, riwayat_file]:
            if not os.path.exists(file):
                with open(file, "w"):
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
                        order_id = parts[0]
                        order_name = parts[1]
                        order_creator = parts[2]
                        order_price = parts[3]
                        order_address = parts[4]
                        order_type = parts[5]
                        order_status = parts[6]
                        if order_creator == self.username:
                            order_display = (
                                f"Pesanan: {order_id} | {order_name} | Rp{order_price} | "
                                f"{order_address} | {order_type} | Status: {order_status}"
                            )
                            self.order_listbox.insert(tk.END, order_display)
        except Exception as e:
            print(f"Error reading {orderan_file}: {e}")
    
    def change_status(self):
        try:
            selected_index = self.order_listbox.curselection()[0]
            order_text = self.order_listbox.get(selected_index)
            order_parts = order_text.split('|')
            order_name = order_parts[1].strip()
            status = order_parts[-1].split(':')[1].strip()
            if status == "sudah dibayar":
                self.prompt_accept_decline(order_name)
            else:
                self.show_status_options(order_name)
        except IndexError:
            messagebox.showwarning("Tidak ada pesanan yang dipilih", "Tolong pilih pesanan.")
    
    def prompt_accept_decline(self, order_name):
        dialog = tk.Toplevel(self)
        dialog.title("Konfirmasi Pesanan")
        dialog.geometry("300x150")
        dialog.configure(bg="#f4f4f4")
        
        label = tk.Label(dialog, text="Terima atau tolak pesanan?", font=("Arial", 12), bg="#f4f4f4")
        label.pack(pady=10)
        
        def accept():
            try:
                with open(posts_file, "r") as post_file:
                    posts = post_file.readlines()
                post_data = None
                for post in posts:
                    post_entry = eval(post.strip()) 
                    if post_entry.get("nama") == order_name:
                        post_data = post_entry
                        break
                if post_data:
                    updated_orders = []
                    order_updated = False
                    with open(orderan_file, "r") as file:
                        orders = file.readlines()
                    with open(orderan_file, "w") as file:
                        for order in orders:
                            parts = order.strip().split(',')
                            if len(parts) >= 7 and parts[1].strip() == order_name and parts[2] == self.username:
                                post_data_str = str(post_data).replace(',', ';')
                                parts[6] = "Pesanan diterima"
                                updated_order = f"{','.join(parts)},{post_data_str}"
                                updated_orders.append(updated_order)
                                order_updated = True
                            else:
                                updated_orders.append(order.strip())
                        file.writelines('\n'.join(updated_orders) + '\n')
                    if order_updated:
                        messagebox.showinfo("Pesanan Diterima", "Status pesanan telah diubah ke 'Pesanan diterima' dan informasi post ditambahkan.")
                    else:
                        messagebox.showwarning("Pesanan Tidak Ditemukan", "Pesanan tidak ditemukan untuk diperbarui.")
                    self.remove_post(order_name)
                    self.load_orders()
                else:
                    messagebox.showerror("Post Tidak Ditemukan", "Informasi post terkait tidak ditemukan.")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan saat menerima pesanan: {e}")
            dialog.destroy()
        
        def decline():
            self.move_to_riwayat(order_name, "Pesanan ditolak")
            self.load_orders()
            dialog.destroy()
        
        accept_button = tk.Button(dialog, text="Terima", font=("Arial", 12), bg="#4caf50", fg="white", command=accept)
        accept_button.pack(side=tk.LEFT, padx=20, pady=10)
        
        decline_button = tk.Button(dialog, text="Tolak", font=("Arial", 12), bg="#f44336", fg="white", command=decline)
        decline_button.pack(side=tk.RIGHT, padx=20, pady=10)
        
        dialog.transient(self)
        dialog.grab_set()
        self.wait_window(dialog)
    
    def show_status_options(self, order_name):
        dialog = tk.Toplevel(self)
        dialog.title("Ubah Status")
        dialog.geometry("300x200")
        dialog.configure(bg="#f4f4f4")
        
        label = tk.Label(dialog, text="Pilih status baru untuk pesanan:", font=("Arial", 12), bg="#f4f4f4")
        label.pack(pady=10)
        
        status_options = ["Pesanan sudah dibungkus", "Pesanan sudah dikirim", "Pesanan sudah sampai"]
        selected_status = tk.StringVar(value=status_options[0])
        
        for option in status_options:
            tk.Radiobutton(
                dialog,
                text=option,
                variable=selected_status,
                value=option,
                font=("Arial", 10),
                bg="#f4f4f4"
            ).pack(anchor="w", padx=20)
        
        def confirm_status():
            new_status = selected_status.get()
            self.update_order_status(order_name, new_status)
            dialog.destroy()
        
        confirm_button = tk.Button(dialog, text="Konfirmasi", font=("Arial", 12), bg="#4caf50", fg="white", command=confirm_status)
        confirm_button.pack(pady=10)
        
        cancel_button = tk.Button(dialog, text="Batal", font=("Arial", 12), bg="#f44336", fg="white", command=dialog.destroy)
        cancel_button.pack(pady=5)
        
        dialog.transient(self)
        dialog.grab_set()
        self.wait_window(dialog)
    
    def update_order_status(self, order_name, new_status):
        updated_orders = []
        status_updated = False
        try:
            with open(orderan_file, "r") as file:
                orders = file.readlines()
            with open(orderan_file, "w") as file:
                for order in orders:
                    parts = order.strip().split(',')
                    if len(parts) >= 7:
                        if parts[1].strip() == order_name and parts[2] == self.username:
                            parts[6] = new_status
                            status_updated = True
                        updated_orders.append(','.join(parts))
                for order in updated_orders:
                    file.write(order + "\n")
            if status_updated:
                messagebox.showinfo("Status Diubah", "Status pesanan telah diubah.")
                self.load_orders()
            else:
                messagebox.showwarning("Gagal Mengubah Status", "Tidak ada pesanan yang ditemukan untuk diubah statusnya.")
        except FileNotFoundError:
            messagebox.showerror("File Tidak Ditemukan", "File orderan.txt tidak ditemukan.")
        except PermissionError:
            messagebox.showerror("Akses Ditolak", "Tidak memiliki izin untuk mengakses file.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat memperbarui status pesanan: {e}")
    
    def move_to_riwayat(self, order_name, status):
        try:
            with open(orderan_file, "r") as file:
                orders = file.readlines()
            with open(posts_file, "r") as post_file:
                posts = post_file.readlines()
            post_data = None
            ordering_user = None
            for order in orders:
                parts = order.strip().split(',')
                if len(parts) >= 7 and parts[1].strip() == order_name:
                    ordering_user = parts[0].strip() 
                    break
            for post in posts:
                post_entry = eval(post.strip())  
                if post_entry.get("nama") == order_name:
                    post_data = post_entry
                    break
            if post_data and ordering_user:
                # Replace commas with semicolons in the post data and status
                post_data_str = str(post_data).replace(',', ';')
                riwayat_entry = f"{post_data_str},{status}"
                self.add_to_riwayat_file(ordering_user, riwayat_entry)
                with open(orderan_file, "w") as file:
                    for order in orders:
                        parts = order.strip().split(',')
                        if len(parts) >= 7 and parts[1].strip() != order_name:
                            file.write(order + "\n")
            else:
                messagebox.showerror("Error", "Pesanan atau post terkait tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat memindahkan ke riwayat: {e}")
    
    def remove_post(self, post_name):
        try:
            updated_posts = []
            post_removed = False
            with open(posts_file, "r") as file:
                posts = file.readlines()
            for post in posts:
                if post.strip():
                    post_data = eval(post.strip()) 
                    if post_data.get("nama") != post_name:
                        updated_posts.append(post)
                    else:
                        post_removed = True
            with open(posts_file, "w") as file:
                file.writelines(updated_posts)
            if post_removed:
                print(f"Post '{post_name}' removed from posts file.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat menghapus post: {e}")
    
    def add_to_riwayat_file(self, ordering_user, entry):
        try:
            riwayat_data = {}
            if os.path.exists(riwayat_file):
                with open(riwayat_file, "r") as file:
                    for line in file:
                        user, order_list = line.strip().split(":", 1)
                        riwayat_data[user] = eval(order_list)
            if ordering_user not in riwayat_data:
                riwayat_data[ordering_user] = []
            riwayat_data[ordering_user].append(entry)
            with open(riwayat_file, "w") as file:
                for user, orders in riwayat_data.items():
                    file.write(f"{user}:{orders}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan ke riwayat: {e}")
    
    def profile(self):
        self.destroy()
        Profile.profile(self.username, self.account_type).mainloop()
