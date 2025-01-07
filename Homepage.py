import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import Profile

posts_file = "posts.txt"
user_data_file = "user_data.txt"

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
                'organisasi': "",
                'No. Tlp': "",
                'alamat': []  
            }
        self.user_info = user_data[username]
        
        self.label_welcome = tk.Label(self, text=f"Selamat datang ke BajuKita, {self.username}", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#333")
        self.label_welcome.pack(pady=20)
        
        self.button_frame = tk.Frame(self, bg="#f4f4f4")
        self.button_frame.pack(pady=20)
        
        self.basket_button = tk.Button(self.button_frame, text="Basket", font=("Arial", 14), bg="#ff6f61", fg="white", command=self.basket)
        self.basket_button.grid(row=0, column=0, padx=10)
        
        self.donasi_button = tk.Button(self.button_frame, text="Donasi", font=("Arial", 14), bg="#D5006D", fg="white", command=self.donasi)
        self.donasi_button.grid(row=0, column=1, padx=10)
        
        self.posts_label = tk.Label(self, text="Post Terbaru:", font=("Arial", 14, "bold"), bg="#f4f4f4", fg="#333")
        self.posts_label.pack(pady=10)
        
        self.post_type_frame = tk.Frame(self, bg="#f4f4f4")
        self.post_type_frame.pack(pady=10)
        
        self.thrift_button = tk.Button(self.post_type_frame, text="Thrift Posts", font=("Arial", 12), bg="#ff9800", fg="white", command=self.load_thrift_posts)
        self.thrift_button.grid(row=0, column=0, padx=10)
        
        self.donation_button = tk.Button(self.post_type_frame, text="Donation Posts", font=("Arial", 12), bg="#8bc34a", fg="white", command=self.load_donation_posts)
        self.donation_button.grid(row=0, column=1, padx=10)
        
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
        self.load_posts() 
    
    def load_user_data(self):
        if os.path.exists(user_data_file):
            with open(user_data_file, "r") as file:
                for line in file:
                    try:
                        parts = line.strip().split(',')
                        if len(parts) < 6:
                            print(f"Skipping malformed line: {line}")
                            continue
                        username = parts[0]
                        basket_count = int(parts[1]) if parts[1].isdigit() else 0 
                        donasi_count = int(parts[2]) if parts[2].isdigit() else 0 
                        organisasi = parts[3]
                        tlp = parts[4]
                        alamat = parts[5].split(';') if parts[5] else []
                        user_data[username] = {
                            'basket': [],
                            'donasi': [],
                            'basket_count': basket_count,
                            'donasi_count': donasi_count,
                            'organisasi': organisasi,
                            'No. Tlp': tlp,
                            'alamat': alamat
                        }
                    except Exception as e:
                        print(f"Error processing line: {line}. Error: {e}")
    
    def save_user_data(self):
        try:
            with open(user_data_file, "w") as file:
                for username, data in user_data.items():
                    basket_count = data['basket_count']
                    donasi_count = data['donasi_count']
                    organisasi = data['organisasi']
                    tlp = data['No. Tlp']
                    alamat = ";".join(data['alamat']) 
                    file.write(f"{username},{basket_count},{donasi_count},{organisasi},{tlp},{alamat}\n")
            print("User data saved successfully.")
        except Exception as e:
            print(f"Error saving user data: {e}")
    
    def ensure_file_exists(self):
        if not os.path.exists(posts_file):
            try:
                with open(posts_file, "w"):
                    pass 
            except Exception as e:
                print(f"Error ensuring posts file exists: {e}")
    
    def basket(self):
        basket_content = "\n".join(self.user_info['basket']) if self.user_info['basket'] else "Tidak ada barang di basket."
        messagebox.showinfo("Basket", f"Barang dalam basket:\n{basket_content}")
    
    def donasi(self):
        donasi_content = "\n".join(self.user_info['donasi']) if self.user_info['donasi'] else "Tidak ada barang di donasi."
        messagebox.showinfo("Donasi", f"Donasi yang ingin dilakukan:\n{donasi_content}")
    
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
                self.save_user_data() 
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
                self.save_user_data()  
            else:
                messagebox.showwarning("Bukan post Donasi", "Hanya post Donasi yang dapat dimasukkan ke dalam donasi.")
        except IndexError:
            messagebox.showwarning("Tidak ada post yang dipilih", "Tolong pilih post untuk ditambahkan ke donasi.")
    
    def update_donasi(self):
        messagebox.showinfo("Tambahan", f"Donasi: {self.user_info['donasi_count']} Donasi yang ingin dilakukan")
    
    def load_thrift_posts(self):
        self.posts_list.delete(0, tk.END)
        for post in self.posts_data:
            if post.get('tipe', '').lower() == 'thrift':
                display_post = f"Post: {post['nama']} | Tempat: {post['tempat']} | Organisasi/Toko: {post['organisasi']} | Tipe: {post['tipe']} | Deskripsi: {post['deskripsi']}"
                self.posts_list.insert(tk.END, display_post)
    
    def load_donation_posts(self):
        self.posts_list.delete(0, tk.END)
        for post in self.posts_data:
            if post.get('tipe', '').lower() == 'donasi':
                display_post = f"Post: {post['nama']} | Tempat: {post['tempat']} | Organisasi/Toko: {post['organisasi']} | Tipe: {post['tipe']} | Deskripsi: {post['deskripsi']}"
                self.posts_list.insert(tk.END, display_post)
    
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
    
    def profile(self, username, account_type):
        self.destroy()
        Profile.profile(username, account_type).mainloop()

if __name__ == "__main__":
    app = Homepage(username="Seller1", account_type="penjual")
    app.mainloop()
