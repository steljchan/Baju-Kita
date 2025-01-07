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
                'organisasi': "",
                'No. Tlp': "",
                'alamat': []  
            }
        self.user_info = user_data[username]
        self.organisasi = self.user_info['organisasi']
        self.tlp = self.user_info['No. Tlp']
        self.alamat = self.user_info['alamat']
        
        self.update_button = tk.Button(self, text="Edit Info", font=("Arial", 12), bg="#4caf50", fg="white", command=self.update_info)
        self.update_button.pack(pady=10)
        
        self.manage_address_button = tk.Button(self, text="Daftar Alamat", font=("Arial", 12), bg="#4caf50", fg="white", command=self.list_alamat)
        self.manage_address_button.pack(pady=10)
        
        self.logout_button = tk.Button(self, text="Logout", font=("Arial", 12), bg="#4caf50", fg="white", command=self.logout)
        self.logout_button.pack(pady=10)
        
        self.back_button = tk.Button(self, text="Kembali", font=("Arial", 12), bg="#9e9e9e", fg="white", command=self.back_to_profile)
        self.back_button.pack(pady=10)
    
    def update_info(self):
        new_organisasi = simpledialog.askstring("Input", "Masukkan Organisasi/Toko baru:", initialvalue=self.organisasi)
        new_tlp = simpledialog.askstring("Input", "Masukkan No. Tlp baru:", initialvalue=self.tlp)
        
        if new_tlp:
            self.tlp = new_tlp
            self.user_info['No. Tlp'] = new_tlp
        if new_organisasi:
            self.organisasi = new_organisasi
            self.user_info['organisasi'] = new_organisasi
        
        self.update_profile_info()
        self.save_user_data()
        messagebox.showinfo("Profile Updated", "Your profile has been successfully updated!")
    
    def update_profile_info(self):
        self.organisasi_label.config(text=f"Organisasi/Toko: {self.organisasi}")
        self.tlp_label.config(text=f"No. Tlp: {self.tlp}")
    
    def list_alamat(self):
        self.withdraw() 
        alamat_window = List_Alamat.Alamat(self.username, self.account_type, self.alamat)
        alamat_window.protocol("WM_DELETE_WINDOW", self.on_alamat_window_close)
        alamat_window.mainloop()

    def on_alamat_window_close(self):
        self.deiconify()  
        self.update_profile_info()
    
    def save_user_data(self):
        global user_data
        with open(user_data_file, "w") as file:
            for username, data in user_data.items():
                basket_count = data['basket_count']
                donasi_count = data['donasi_count']
                organisasi = data['organisasi']
                tlp = data['No. Tlp']
                alamat = ";".join(data['alamat']) 
                file.write(f"{username},{basket_count},{donasi_count},{organisasi},{tlp},{alamat}\n")
    
    def logout(self):
        self.destroy()
        messagebox.showinfo("Logged Out", "You have successfully logged out!")
    
    def back_to_profile(self):
        self.destroy() 
        Profile.profile(self.username, self.account_type).mainloop()

    def ensure_file_exists(self):
        if not os.path.exists(user_data_file):
            with open(user_data_file, "w"):
                pass  # Create an empty user data file if it doesn't exist

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

if __name__ == "__main__":
    app = settings(username="Seller1", account_type="seller")
    app.mainloop()
