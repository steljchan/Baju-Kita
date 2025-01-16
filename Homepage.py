import tkinter as tk
import ast 
from tkinter import simpledialog, messagebox
import os
import Profile
import Keranjang

posts_file = "posts.txt"
user_data_file = "user_data.txt"
basket_file = "basket.txt"
donasi_file = "donasi.txt"
orderan_file = "orderan.txt"
user_data = {}

class Homepage(tk.Tk):
    def __init__(self, username, account_type):
        super().__init__()
        self.title("Baju Kita")
        self.geometry("800x600")
        self.configure(bg="#f4f4f4")
        self.username = username
        self.account_type = account_type
        self.load_user_data()  
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
        
        self.label_welcome = tk.Label(self, text=f"Selamat datang ke BajuKita, {self.username}", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#333")
        self.label_welcome.pack(pady=20)
        
        self.button_frame = tk.Frame(self, bg="#f4f4f4")
        self.button_frame.pack(pady=20)
        
        self.basket_button = tk.Button(self, text="Basket", font=("Arial", 14), bg="#ff6f61", fg="white", command=lambda: self.basket(self.username, self.account_type))
        self.basket_button.place(x=680, y=20) 
        self.bind(
            "<Configure>", 
            lambda event: self.basket_button.place(
                x=self.winfo_width() - 120, 
                y=20
            )
        )
        
        self.donasi_button = tk.Button(self.button_frame, text="Donasi", font=("Arial", 14), bg="#D5006D", fg="white", command=self.donasi)
        self.donasi_button.grid(row=0, column=1, padx=10)
        
        self.posts_label = tk.Label(self, text="Post Terbaru:", font=("Arial", 14, "bold"), bg="#f4f4f4", fg="#333")
        self.posts_label.pack(pady=10)
        
        self.post_type_frame = tk.Frame(self, bg="#f4f4f4")
        self.post_type_frame.pack(pady=10)
        
        self.posts_list = tk.Listbox(self, font=("Arial", 12), width=60, height=10) 
        self.posts_list.pack(pady=10)
        
        self.post_frame = tk.Frame(self, bg="#f4f4f4")
        self.post_frame.pack(pady=10)
        
        self.view_post_button = tk.Button(self.post_frame, text="Lihat Post", font=("Arial", 12), bg="#ff9800", fg="white", command=self.view_post)
        self.view_post_button.grid(row=0, column=0, padx=10)
        
        self.add_to_basket_button = tk.Button(self.post_frame, text="Tambahkan ke Basket", font=("Arial", 12), bg="#2196f3", fg="white", command=self.tambahkan_dalam_basket)
        self.add_to_basket_button.grid(row=0, column=1, padx=10)
        
        self.add_to_donasi_button = tk.Button(self.post_frame, text="Tambahkan ke Donasi", font=("Arial", 12), bg="#8bc34a", fg="white", command=self.tambahkan_isi_donasi)
        self.add_to_donasi_button.grid(row=0, column=2, padx=10)
        
        self.profil_button = tk.Button(self.post_frame, text="Profil", font=("Arial", 12), bg="#8bc34a", fg="white", command=lambda: self.profile(self.username, self.account_type))
        self.profil_button.grid(row=0, column=3, padx=10)
        
        self.ensure_file_exists() 
        self.load_thrift_posts() 
    
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
    
    def save_user_data(self):
        with open(user_data_file, "w") as f:
            for username, data in user_data.items():
                basket_count = data['basket_count']
                donasi_count = data['donasi_count']
                kelamin = data['kelamin']
                organisasi = data['organisasi']
                tlp = data['No. Tlp']
                email = data['email']
                alamat = ";".join(data['alamat']) if data['alamat'] else "" 
                f.write(f"{username},{basket_count},{donasi_count},{kelamin},{organisasi},{tlp},{email},{alamat}\n")
    
    def ensure_file_exists(self):
        if not os.path.exists(posts_file):
            try:
                with open(posts_file, "w"):  
                    pass
            except Exception as e:
                print(f"Error ensuring posts file exists: {e}")
    
    def basket(self, username, account_type):
        self.destroy()
        Keranjang.basket(username, account_type).mainloop()
    
    def donasi(self, username, account_type):
        pass
    
    def view_post(self):
        try:
            selected_index = self.posts_list.curselection()[0]
            post = self.posts_list.get(selected_index)
            messagebox.showinfo("Deskripsi Post", f"{post}")
            if "thrift" in post.lower():
                self.add_to_basket_button.config(state=tk.NORMAL)
                self.add_to_donasi_button.config(state=tk.DISABLED)
            elif "donasi" in post.lower():
                self.add_to_donasi_button.config(state=tk.NORMAL)
                self.add_to_basket_button.config(state=tk.DISABLED)
        except IndexError:
            messagebox.showwarning("Tidak ada post yang dipilih", "Tolong pilih post yang ingin dilihat.")
    
    def save_user_basket(self):
        try:
            with open(basket_file, "a") as file:
                for item in self.user_info['basket']:
                    formatted_entry = f"{self.username}, " + str({
                        'nama': item.get('nama', 'Unknown'),
                        'kategori': item.get('kategori', 'Unknown'),
                        'tempat': item.get('tempat', 'Unknown'),
                        'organisasi': item.get('organisasi', 'Unknown'),
                        'tipe': item.get('tipe', 'Unknown'),
                        'harga': item.get('harga', 'Unknown'),
                        'deskripsi': item.get('deskripsi', 'Unknown'),
                        'creator': item.get('creator', 'Unknown'),
                    })
                    file.write(formatted_entry + "\n")
            print("Basket saved successfully.")
        except Exception as e:
            print(f"Error saving basket: {e}")
    
    def tambahkan_dalam_basket(self):
        try:
            selected_index = self.posts_list.curselection()[0]
            post = self.posts_data[selected_index]  
            if post.get('tipe', '').lower() == 'thrift':
                if any(basket_post.get('nama') == post.get('nama') and basket_post.get('creator') == post.get('creator') for basket_post in self.user_info['basket']):
                    messagebox.showwarning("Post Sudah Ada di Basket", "Post ini sudah ada di dalam basket.")
                    return
                self.user_info['basket'].append(post)
                self.user_info['basket_count'] += 1
                self.save_user_basket()
                messagebox.showinfo("Ditambahkan ke Basket", f"'{post['nama']}' sudah ditambahkan ke dalam basket.")
                self.update_basket()
                self.save_user_data() 
            else:
                messagebox.showwarning("Bukan post Thrift", "Hanya post Thrift yang dapat dimasukkan ke dalam basket.")
        except IndexError:
            messagebox.showwarning("Tidak ada post yang dipilih", "Tolong pilih post untuk ditambahkan ke basket.")
    
    def tambahkan_isi_donasi(self):
        try:
            selected_index = self.posts_list.curselection()[0]
            post = self.posts_data[selected_index] 
            if post.get('tipe', '').lower() == 'donasi':
                if any(donasi_post.get('nama') == post.get('nama') and donasi_post.get('creator') == post.get('creator') for donasi_post in self.user_info['donasi']):
                    messagebox.showwarning("Post Sudah Ada di Donasi", "Post ini sudah ada di dalam daftar donasi.")
                    return
                self.user_info['donasi'].append(post)
                self.user_info['donasi_count'] += 1
                donasi_entry = {
                    "pelanggan": self.username,
                    "post": post,
                    "creator": post.get('creator', 'Unknown') 
                }
                self.save_to_file(donasi_file, donasi_entry)
                messagebox.showinfo("Ditambahkan ke Donasi", f"'{post['nama']}' sudah ditambahkan ke dalam daftar donasi.")
                self.update_donasi()
                self.save_user_data() 
            else:
                messagebox.showwarning("Bukan post Donasi", "Hanya post Donasi yang dapat dimasukkan ke dalam daftar donasi.")
        except IndexError:
            messagebox.showwarning("Tidak ada post yang dipilih", "Tolong pilih post untuk ditambahkan ke donasi.")
    
    def save_to_file(self, file_name, entry):
        try:
            with open(file_name, "a") as file:
                file.write(f"{entry}\n")
        except Exception as e:
            print(f"Error saving to {file_name}: {e}")
    
    def update_basket(self):
        messagebox.showinfo("Tambahan", f"Basket: {self.user_info['basket_count']} Barang")
    
    def update_donasi(self):
        messagebox.showinfo("Tambahan", f"Donasi: {self.user_info['donasi_count']} Donasi yang ingin dilakukan")
    
    def load_thrift_posts(self):
        self.posts_list.delete(0, tk.END)
        self.posts_data = []
        try:
            with open(posts_file, "r") as file:
                posts_list_data = file.readlines()
                for post in posts_list_data:
                    try:
                        post_dict = ast.literal_eval(post.strip())
                        if isinstance(post_dict, dict) and post_dict.get('tipe', '').lower() == 'thrift':
                            nama = post_dict.get('nama', 'Unknown')
                            kategori = post_dict.get('kategori', 'Unknown')
                            tempat = post_dict.get('tempat', 'Unknown')
                            organisasi = post_dict.get('organisasi', 'Unknown')
                            tipe = post_dict.get('tipe', 'Unknown')
                            deskripsi = post_dict.get('deskripsi', 'Unknown')
                            harga = post_dict.get('harga', 'Unknown')
                            if not harga.replace('.', '', 1).isdigit():  
                                harga = 'Invalid Price'
                            display_post = (
                                f"Post: {nama} | Kategori: {kategori} | Tempat: {tempat} | "
                                f"Organisasi/Toko: {organisasi} | Tipe: {tipe} | Harga: {harga} | "
                                f"Deskripsi: {deskripsi}"
                            )
                            self.posts_data.append(post_dict)
                            self.posts_list.insert(tk.END, display_post)
                    except (SyntaxError, ValueError) as e:
                        print(f"Skipping invalid post entry: {post.strip()} | Error: {e}")
        except FileNotFoundError:
            print(f"File '{posts_file}' not found, starting with an empty list.")
    
    def save_to_file(self, file_name, entry):
        try:
            with open(file_name, "a") as file:
                file.write(f"{entry}\n")
            print(f"Entry saved to {file_name}: {entry}")
        except Exception as e:
            print(f"Error saving to {file_name}: {e}")
    
    def profile(self, username, account_type):
        self.destroy()
        Profile.profile(username, account_type).mainloop()

if __name__ == "__main__":
    app = Homepage(username="Seller1", account_type="penjual")
    app.mainloop()