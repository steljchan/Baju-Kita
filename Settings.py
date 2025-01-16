import tkinter as tk
from tkinter import simpledialog, messagebox
import List_Alamat 
import Profile
import os

posts_file = "posts.txt"
user_data_file = "user_data.txt"
user_data = {}

class settings(tk.Tk):
    def __init__(self, username, account_type):
        tk.Tk.__init__(self)
        self.title("Settings")
        self.geometry("250x300")
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
        self.kelamin = self.user_info['kelamin']
        self.organisasi = self.user_info['organisasi']
        self.tlp = self.user_info['No. Tlp']
        self.email = self.user_info['email']
        self.alamat = self.user_info['alamat']
        
        self.update_button = tk.Button(self, text="Edit Info", font=("Arial", 12), bg="#4caf50", fg="white", command=self.update_info)
        self.update_button.pack(pady=10)
        
        self.manage_address_button = tk.Button(self, text="Daftar Alamat", font=("Arial", 12), bg="#4caf50", fg="white", command=self.list_alamat)
        self.manage_address_button.pack(pady=10)
        
        self.logout_button = tk.Button(self, text="Logout", font=("Arial", 12), bg="#4caf50", fg="white", command=self.logout)
        self.logout_button.pack(pady=10)
        
        self.back_button = tk.Button(self, text="Kembali", font=("Arial", 12), bg="#9e9e9e", fg="white", command=self.back_to_profile)
        self.back_button.pack(pady=10)
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def update_info(self):
        new_kelamin = simpledialog.askstring("Input", "Masukkan jenis kelamin:", initialvalue=self.kelamin)
        if self.account_type == "seller":
            new_organisasi = simpledialog.askstring("Input", "Masukkan Organisasi/Toko baru:", initialvalue=self.organisasi)
        else:
            new_organisasi = "kosong" 
        new_tlp = simpledialog.askstring("Input", "Masukkan No. Tlp baru:", initialvalue=self.tlp)
        new_email = simpledialog.askstring("Input", "Masukkan Email baru:", initialvalue=self.email)
        
        if new_tlp:
            self.tlp = new_tlp
        if new_organisasi and self.account_type == "seller":  
            self.organisasi = new_organisasi
        if new_email:
            self.email = new_email
        if new_kelamin:
            self.kelamin = new_kelamin
        
        self.user_info.update({
            'No. Tlp': self.tlp,
            'organisasi': self.organisasi,
            'email': self.email,
            'kelamin': self.kelamin,
        })
        user_data[self.username] = self.user_info
        
        self.save_user_data()
        messagebox.showinfo("Profil diperbarui", "Profil anda sudah diperbarui!")
    
    def list_alamat(self):
        self.withdraw() 
        alamat_window = List_Alamat.Alamat(self.username, self.account_type, self.alamat)
        alamat_window.protocol("WM_DELETE_WINDOW", self.on_alamat_window_close)
        alamat_window.mainloop()
    
    def on_alamat_window_close(self):
        self.deiconify()
        self.update_profile_info()
    
    def save_user_data(self):
        with open(user_data_file, "w") as f:
            for username, data in user_data.items():
                basket_count = data.get('basket_count', 0)
                donasi_count = data.get('donasi_count', 0)
                kelamin = data.get('kelamin', "")
                organisasi = data.get('organisasi', "")
                tlp = data.get('No. Tlp', "")
                email = data.get('email', "")
                alamat = ";".join(data.get('alamat', []))
                f.write(f"{username},{basket_count},{donasi_count},{kelamin},{organisasi},{tlp},{email},{alamat}\n")
    
    def logout(self):
        self.save_user_data()  
        self.destroy() 
        from Login import App
        app = App()  
        app.mainloop()  
    
    def back_to_profile(self):
        self.save_user_data()
        self.destroy()
        Profile.profile(self.username, self.account_type).mainloop()
    
    def ensure_file_exists(self):
        if not os.path.exists(user_data_file):
            with open(user_data_file, "w"):
                pass
    
    def load_user_data(self):
        global user_data
        user_data.clear()
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
        else:
            print(f"File {user_data_file} not found. Initializing empty user data.")
    
    def on_closing(self):
        self.save_user_data()
        self.destroy()


if __name__ == "__main__":
    app = settings(username="Seller1", account_type="seller")
    app.mainloop()
