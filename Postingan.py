import tkinter as tk
from tkinter import messagebox, simpledialog
import ast
import Profile
import os
from functions.posts import edit_post, remove_post

posts_file = "posts.txt"
user_data_file = "user_data.txt"
basket_file = "basket.txt"
donasi_file = "donasi.txt"
user_data = {}

class my_posts(tk.Tk):
    def __init__(self, username, account_type):
        tk.Tk.__init__(self)
        self.title("Profile")
        self.geometry("800x700") 
        self.configure(bg="#f4f4f4")
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
        self.posts_data = []
        self.load_posts()
        
        self.label_title = tk.Label(self, text=f"Posts by {self.username}", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#333")
        self.label_title.pack(pady=20)
        
        self.posts_listbox = tk.Listbox(self, font=("Arial", 12), width=80, height=20)
        self.posts_listbox.pack(pady=10)
        
        self.show_my_posts()
        
        self.add_post_button = tk.Button(self, text="Add Post", font=("Arial", 12), bg="#4caf50", fg="white", command=self.add_post)
        self.add_post_button.pack(pady=10)
        
        self.edit_post_button = tk.Button(self, text="Edit Post", font=("Arial", 12), bg="#00008B", fg="white", command=self.edit_post)
        self.edit_post_button.pack(pady=10)
        
        self.close_button = tk.Button(self, text="Kembali", font=("Arial", 12), bg="#ff6f61", fg="white", command=self.back)
        self.close_button.place(x=600, y=20)
        
        self.remove_post_button = tk.Button(self, text="Remove Post", font=("Arial", 12), bg="#f44336", fg="white", command=self.remove_post)
        self.remove_post_button.pack(pady=10)
        
        self.load_user_data()
    
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
    
    def load_posts(self):
        self.posts_data = []  
        try:
            if os.path.exists(posts_file):
                with open(posts_file, "r") as file:
                    posts_list_data = file.readlines()
                    for post in posts_list_data:
                        try:
                            post_dict = ast.literal_eval(post.strip())
                            if isinstance(post_dict, dict):
                                self.posts_data.append(post_dict)
                        except (SyntaxError, ValueError) as e:
                            print(f"Skipping invalid post entry: {post.strip()} | Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading posts: {e}")
    
    def show_my_posts(self):
        self.posts_listbox.delete(0, tk.END)
        for post in self.posts_data:
            if post.get("creator", "") == self.username:
                display_post = (
                    f"Post: {post['nama']} | Kategori: {post.get('kategori', 'N/A')} | Tempat: {post['tempat']} | "
                    f"Organisasi: {post['organisasi']} | Tipe: {post['tipe']} | "
                    f"Harga: {post.get('harga', 'N/A')} | Deskripsi: {post['deskripsi']}"
                )
                self.posts_listbox.insert(tk.END, display_post)
    
    def add_post(self):
        organisasi = user_data.get(self.username, {}).get("organisasi", "")
        if not organisasi:
            messagebox.showwarning("Data Missing", "Organisasi tidak ditemukan dalam data pengguna.")
            return
        nama_post = simpledialog.askstring("Input", "Masukkan nama post: ")
        while True:
            kategori = simpledialog.askstring("Input", "Masukkan kategori baju (bayi, balita, anak-anak, remaja, dewasa):")
            if kategori and kategori.lower() in ['bayi', 'balita', 'anak-anak', 'remaja', 'dewasa']:
                break
            else:
                messagebox.showwarning("Kategori salah", "Kategori harus 'bayi', 'balita', 'anak-anak', 'remaja', atau 'dewasa'.")
        tipe_post = "Thrift"
        tempat = simpledialog.askstring("Input", "Masukkan tempat (Nama kota): ")
        organisasi = user_data[self.username].get('organisasi', '')
        if not organisasi:
            organisasi = simpledialog.askstring("Input", "Masukkan nama toko (organisasi):")
            if not organisasi:
                messagebox.showwarning("Input Salah", "Organisasi tidak boleh kosong!")
        deskripsi = simpledialog.askstring("Input", "Masukkan deskripsi (Jenis baju-Jenis kain-Size): ")
        harga = simpledialog.askstring("Input", "Masukkan harga baju: ")
        post_details = {
            "nama": nama_post,
            "kategori": kategori,
            "tempat": tempat,
            "organisasi": organisasi,
            "tipe": tipe_post,
            "harga": harga,
            "deskripsi": deskripsi,
            "creator": self.username
        }
        self.posts_listbox.insert(
            tk.END,
            f"Post: {nama_post} | Kategori: {kategori} | Tempat: {tempat} | Organisasi/Toko: {organisasi} | Tipe: {tipe_post} | Harga: {harga} | Deskripsi: {deskripsi}"
        )
        with open(posts_file, "a") as file:
            file.write(str(post_details) + "\n")
        messagebox.showinfo("Post Ditambahkan", f"Post '{nama_post}' telah berhasil ditambahkan!")
    
    def edit_post(self):
        edit_post(self)
    
    def remove_post(self):
        remove_post(self)
    
    def remove_from_file(self, file_name, removed_post):
        if os.path.exists(file_name):
            updated_entries = []
            with open(file_name, "r") as file:
                for line in file:
                    try:
                        entry = eval(line.strip())
                        if entry['post']['nama'] != removed_post['nama'] or entry['post']['creator'] != removed_post['creator']:
                            updated_entries.append(entry)
                    except Exception as e:
                        print(f"Error processing entry in {file_name}: {e}")
            with open(file_name, "w") as file:
                for entry in updated_entries:
                    file.write(str(entry) + "\n")
    
    def back(self):
        self.destroy()  
        self.profile_window()  
    
    def profile_window(self):
        profile_window = Profile.profile(self.username, self.account_type) 
        self.withdraw()  
        profile_window.deiconify()  
        profile_window.lift()  

if __name__ == "__main__":
    app = my_posts(username="User1", account_type="penjual")
    app.mainloop()
