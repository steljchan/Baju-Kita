import tkinter as tk
from tkinter import simpledialog, messagebox
import Settings
import Homepage
import Postingan
import os

posts_file = "posts.txt"
user_data_file = "user_data.txt"
user_data = {}

class profile(tk.Tk):
    def __init__(self, username, account_type):
        tk.Tk.__init__(self)
        self.title("Profile")
        self.geometry("675x500") 
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
                'organisasi': "",
                'No. Tlp': "",
                'alamat': []  
            }
        self.user_info = user_data[username]
        self.organisasi = self.user_info['organisasi']
        self.tlp = self.user_info['No. Tlp']
        self.alamat = self.user_info['alamat']
        
        self.label_profile = tk.Label(self, text="Profil", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#333")
        self.label_profile.pack(pady=20)
        
        self.nama_label = tk.Label(self, text=f"Username: {self.username}", font=("Arial", 14, "bold"), bg="#f4f4f4", fg="#333")
        self.nama_label.pack(pady=10)
        
        self.organisasi_label = tk.Label(self, text=f"Organisasi/Toko: {self.organisasi}", font=("Arial", 14, "bold"), bg="#f4f4f4", fg="#333")
        self.organisasi_label.pack(pady=10)
        
        self.tlp_label = tk.Label(self, text=f"No. Tlp: {self.tlp}", font=("Arial", 14, "bold"), bg="#f4f4f4", fg="#333")
        self.tlp_label.pack(pady=10)
        
        main_address = self.alamat[0] if self.alamat else "Tidak ada alamat diset"
        self.alamat_label = tk.Label(self, text=f"Alamat Utama: {main_address}", font=("Arial", 14, "bold"), bg="#f4f4f4", fg="#333")
        self.alamat_label.pack(pady=10)
        
        self.riwayat_button = tk.Button(self, text="Riwayat Belanja", font=("Arial", 12), bg="#4caf50", fg="white", command=self.riwayat)
        self.riwayat_button.pack(pady=10)
        
        self.pesanan_button = tk.Button(self, text="Pesanan Anda", font=("Arial", 12), bg="#4caf50", fg="white", command=self.pesanan)
        self.pesanan_button.pack(pady=10)
        
        if self.account_type == 'seller':
            self.postingan_button = tk.Button(self, text="Postingan Anda", font=("Arial", 12), bg="#4caf50", fg="white", command=self.postingan)
            self.postingan_button.pack(pady=10)
        
        self.settings_button = tk.Button(self, text="Settings", font=("Arial", 12), bg="#4caf50", fg="white", command=self.settings)
        self.settings_button.place(x=600, y=20)
        
        self.homepage_button = tk.Button(self, text="Homepage", font=("Arial", 12), bg="#4caf50", fg="white", command=self.homepage)
        self.homepage_button.pack(pady=10)
    
    def update_info(self):
        new_organisasi = simpledialog.askstring("Input", "Masukkan Organisasi/Toko baru:", initialvalue=self.organisasi)
        new_tlp = simpledialog.askstring("Input", "Masukkan No. Tlp baru:", initialvalue=self.tlp)
        if new_tlp:
            self.tlp = new_tlp
            self.user_info['No. Tlp'] = new_tlp
        if new_organisasi:
            self.organisasi = new_organisasi
            self.user_info['organisasi'] = new_organisasi
        self.organisasi_label.config(text=f"Store: {self.organisasi}")
        self.tlp_label.config(text=f"Phone: {self.tlp}")
        self.save_user_data()
        messagebox.showinfo("Profile Updated", "Your profile has been successfully updated!")
    
    def riwayat(self):
        pass
    
    def pesanan(self):
        pass
    
    def postingan(self):
        self.withdraw()  
        settings_window = Postingan.my_posts(self.username, self.account_type) 
        settings_window.protocol("WM_DELETE_WINDOW")
        settings_window.mainloop()
    
    def settings(self):
        self.withdraw()  
        settings_window = Settings.settings(self.username, self.account_type) 
        settings_window.protocol("WM_DELETE_WINDOW", self.on_settings_window_close)
        settings_window.mainloop()
    
    def on_settings_window_close(self):
        self.deiconify()  
        self.update_profile_info()
    
    def update_profile_info(self):
        main_address = self.user_info['alamat'][0] if self.user_info['alamat'] else "Tidak ada alamat diset"
        self.alamat_label.config(text=f"Alamat Utama: {main_address}")
    
    def homepage(self):
        self.destroy()
        Homepage.Homepage(self.username, self.account_type).mainloop()
    
    def ensure_file_exists(self):
        if not os.path.exists(posts_file):
            with open(posts_file, "w"):
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
        with open(user_data_file, "w") as file:
            for username, data in user_data.items():
                basket_count = data['basket_count']
                donasi_count = data['donasi_count']
                organisasi = data['organisasi']
                tlp = data['No. Tlp']
                alamat = ";".join(data['alamat']) 
                file.write(f"{username},{basket_count},{donasi_count},{organisasi},{tlp},{alamat}\n")

if __name__ == "__main__":
    app = profile(username="Seller1", account_type="seller")
    app.mainloop()
