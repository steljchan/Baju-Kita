import tkinter as tk
from tkinter import simpledialog, messagebox
import os

posts_file = "posts.txt"
user_data_file = "user_data.txt"

user_data = {}

def load_user_data():
    if os.path.exists(user_data_file):
        with open(user_data_file, "r") as file:
            for line in file:
                username, basket_count, donasi_count = line.strip().split(',')
                user_data[username] = {
                    'basket': [],
                    'donasi': [],
                    'basket_count': int(basket_count),
                    'donasi_count': int(donasi_count)
                }

def save_user_data():
    with open(user_data_file, "w") as file:
        for username, data in user_data.items():
            basket_count = data['basket_count']
            donasi_count = data['donasi_count']
            file.write(f"{username},{basket_count},{donasi_count}\n")

def ensure_file_exists():
    if not os.path.exists(posts_file):
        with open(posts_file, "w"):
            pass

class Homepage(tk.Tk):
    def __init__(self, username, account_type):
        super().__init__()
        self.title("Baju Kita")
        self.geometry("800x600")
        self.configure(bg="#f4f4f4")
        
        self.username = username
        self.account_type = account_type

        if username not in user_data:
            user_data[username] = {
                'basket': [],
                'donasi': [],
                'basket_count': 0,
                'donasi_count': 0
            }
        self.user_info = user_data[username]

        self.label_welcome = tk.Label(self, text=f"Selamat datang ke BajuKita, {self.username}", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#333")
        self.label_welcome.pack(pady=20)
        
        self.button_frame = tk.Frame(self, bg="#f4f4f4")
        self.button_frame.pack(pady=20)
        
        self.shop_button = tk.Button(self.button_frame, text="Basket", font=("Arial", 14), bg="#ff6f61", fg="white", command=self.basket)
        self.shop_button.grid(row=0, column=0, padx=10)
        
        self.donasi_button = tk.Button(self.button_frame, text="Donasi", font=("Arial", 14), bg="#D5006D", fg="white", command=self.donasi)
        self.donasi_button.grid(row=0, column=1, padx=10)
        
        self.posts_label = tk.Label(self, text="Post Terbaru:", font=("Arial", 14, "bold"), bg="#f4f4f4", fg="#333")
        self.posts_label.pack(pady=10)
        
        self.posts_list = tk.Listbox(self, font=("Arial", 12), width=60, height=10) 
        self.posts_list.pack(pady=10)
        
        self.post_frame = tk.Frame(self, bg="#f4f4f4")
        self.post_frame.pack(pady=10)
        
        if self.account_type == 'seller':
            self.add_post_button = tk.Button(self.post_frame, text="Tambahkan Post", font=("Arial", 12), bg="#4caf50", fg="white", command=self.add_post)
            self.add_post_button.grid(row=0, column=0, padx=10)
            
            self.edit_post_button = tk.Button(self.post_frame, text="Edit Post", font=("Arial", 12), bg="#00008B", fg="white", command=self.edit_post)
            self.edit_post_button.grid(row=0, column=1, padx=10)
        
        self.view_post_button = tk.Button(self.post_frame, text="Lihat Post", font=("Arial", 12), bg="#ff9800", fg="white", command=self.view_post)
        self.view_post_button.grid(row=0, column=2, padx=10)
        
        self.add_to_basket_button = tk.Button(self.post_frame, text="Tambahkan ke Basket", font=("Arial", 12), bg="#2196f3", fg="white", command=self.tambahkan_dalam_basket)
        self.add_to_basket_button.grid(row=0, column=3, padx=10)
        
        self.add_to_donasi_button = tk.Button(self.post_frame, text="Tambahkan ke Donasi", font=("Arial", 12), bg="#8bc34a", fg="white", command=self.tambahkan_isi_donasi)
        self.add_to_donasi_button.grid(row=0, column=4, padx=10)
        
        ensure_file_exists()
        self.load_posts() 
    
    def basket(self):
        basket_content = "\n".join(self.user_info['basket']) if self.user_info['basket'] else "Tidak ada barang di basket."
        messagebox.showinfo("Basket", f"Barang dalam basket:\n{basket_content}")
    
    def donasi(self):
        donasi_content = "\n".join(self.user_info['donasi']) if self.user_info['donasi'] else "Tidak ada barang di donasi."
        messagebox.showinfo("Donasi", f"donasi yang ingin dilakukan:\n{donasi_content}")
    
    def add_post(self):
        nama_post = simpledialog.askstring("Input", "Masukkan nama post: ")
        while True:
            tipe_post = simpledialog.askstring("Input", "Masukkan tipe post (Thrift atau Donasi): ")
            if tipe_post.lower() not in ["thrift", "donasi"]:
                messagebox.showwarning("Tipe post salah", "Tipe post harus 'Thrift' atau 'Donasi'.")
            elif tipe_post.lower() in ["thrift", "donasi"]:
                break
        if tipe_post.lower() == "thrift":
            tempat = simpledialog.askstring("Input", "Masukkan tempat (Nama kota): ")
            organisasi = simpledialog.askstring("Input", "Masukkan nama toko: ")
            deskripsi = simpledialog.askstring("Input", "Masukkan deskripsi (Jenis baju, Jenis kain, Harga baju): ")
        else:
            tempat = simpledialog.askstring("Input", "Masukkan tempat (Nama jalan, Nama kota): ")
            organisasi = simpledialog.askstring("Input", "Masukkan nama organisasi: ")
            deskripsi = simpledialog.askstring("Input", "Masukkan deskripsi (Jenis baju yang dibutuhkan, Jenis kain yang diinginkan, tujuan donasi): ")
        if not nama_post or not tempat or not organisasi or not tipe_post or not deskripsi:
            messagebox.showwarning("Informasi post tidak lengkap", "Tolong isi semua informasi (nama, tempat, organisasi, tipe, dan deskripsi).")
            return
        post_details = {
            "nama": nama_post,
            "tempat": tempat,
            "organisasi": organisasi,
            "tipe": tipe_post,
            "deskripsi": deskripsi,
            "creator": self.username
        }
        self.posts_list.insert(tk.END, f"Post: {nama_post} | Tempat: {tempat} | Organisasi/Toko: {organisasi} | Tipe: {tipe_post} | Deskripsi: {deskripsi}")
        with open(posts_file, "a") as file:
            file.write(str(post_details) + "\n")
        messagebox.showinfo("Post Ditambahkan", f"Post '{nama_post}' telah berhasil ditambahkan!")
    
    def edit_post(self):
        try:
            selected_index = self.posts_list.curselection()[0]
            post_display = self.posts_list.get(selected_index)
            post_details = self.posts_data[selected_index]
            if post_details['creator'] != self.username:
                messagebox.showwarning("Tidak memiliki hak", "Anda hanya bisa mengedit post yang Anda buat.")
                return
            new_nama_post = simpledialog.askstring("Edit Post", f"Edit nama post ({post_details['nama']}):") or post_details['nama']
            new_tempat = simpledialog.askstring("Edit Post", f"Edit tempat ({post_details['tempat']}):") or post_details['tempat']
            new_organisasi = simpledialog.askstring("Edit Post", f"Edit organisasi/toko ({post_details['organisasi']}):") or post_details['organisasi']
            new_deskripsi = simpledialog.askstring("Edit Post", f"Edit deskripsi ({post_details['deskripsi']}):") or post_details['deskripsi']
            post_details['nama'] = new_nama_post
            post_details['tempat'] = new_tempat
            post_details['organisasi'] = new_organisasi
            post_details['deskripsi'] = new_deskripsi
            self.posts_list.delete(selected_index)
            self.posts_list.insert(selected_index, f"Post: {new_nama_post} | Tempat: {new_tempat} | Organisasi/Toko: {new_organisasi} | Tipe: {post_details['tipe']} | Deskripsi: {new_deskripsi}")
            with open(posts_file, "w") as file:
                for post in self.posts_data:
                    file.write(str(post) + "\n")
            messagebox.showinfo("Post Diedit", "Post berhasil diedit!")
        except IndexError:
            messagebox.showwarning("Tidak ada post yang dipilih", "Tolong pilih post yang ingin diedit.")
    
    def view_post(self):
        try:
            selected_index = self.posts_list.curselection()[0]
            post = self.posts_list.get(selected_index)
            messagebox.showinfo("Deskripsi Post", f"{post}")
        except IndexError:
            messagebox.showwarning("Tidak ada post yang dipilih", "Tolong pilih post yang ingin dilihat.")
    
    def tambahkan_dalam_basket(self):
        try:
            selected_index = self.posts_list.curselection()[0]
            post = self.posts_list.get(selected_index)
            if "thrift" in post.lower():
                self.user_info['basket'].append(post)
                self.user_info['basket_count'] += 1
                messagebox.showinfo("Ditambahkan ke Basket", f"'{post}' sudah ditambahkan ke dalam basket.")
                self.update_basket()
            else:
                messagebox.showwarning("Bukan post Thrift", "Hanya post Thrift yang dapat dimasukkan ke dalam basket.")
        except IndexError:
            messagebox.showwarning("Tidak ada post yang dipilih", "Tolong pilih post untuk ditambahkan ke basket.")
    
    def update_basket(self):
        messagebox.showinfo("Tambahan", f"Basket: {self.user_info['basket_count']} Barang")
    
    def tambahkan_isi_donasi(self):
        try:
            selected_index = self.posts_list.curselection()[0]
            post = self.posts_list.get(selected_index)
            if "donasi" in post.lower():
                self.user_info['donasi'].append(post)
                self.user_info['donasi_count'] += 1
                messagebox.showinfo("Ditambahkan ke Donasi", f"'{post}' sudah ditambahkan ke dalam donasi.")
                self.update_donasi()
            else:
                messagebox.showwarning("Bukan post Donasi", "Hanya post Donasi yang dapat dimasukkan ke dalam donasi.")
        except IndexError:
            messagebox.showwarning("Tidak ada post yang dipilih", "Tolong pilih post untuk ditambahkan ke donasi.")
    
    def update_donasi(self):
        messagebox.showinfo("Tambahan", f"Donasi: {self.user_info['donasi_count']} Donasi yang ingin dilakukan")
    
    def load_posts(self):
        self.posts_list.delete(0, tk.END) 
        self.posts_data = []
        try:
            with open(posts_file, "r") as file:
                posts_list_data = file.readlines()
                for post in posts_list_data:
                    post_dict = eval(post.strip())
                    if isinstance(post_dict, dict) and 'nama' in post_dict:
                        display_post = f"Post: {post_dict['nama']} | Tempat: {post_dict['tempat']} | Organisasi/Toko: {post_dict['organisasi']} | Tipe: {post_dict['tipe']} | Deskripsi: {post_dict['deskripsi']}"
                        self.posts_data.append(post_dict)
                        self.posts_list.insert(tk.END, display_post)
                print(self.posts_list)
        except FileNotFoundError:
            print(f"File '{posts_file}' not found, starting with an empty list.")

if __name__ == "__main__":
    load_user_data()
    app = Homepage(username="Seller1", account_type="penjual")
    app.mainloop()
    save_user_data()
