import tkinter as tk
from tkinter import simpledialog, messagebox
import Settings
import os

user_data_file = "user_data.txt"  

user_data = {}  

class Alamat(tk.Toplevel):
    def __init__(self, username, account_type, alamat):
        super().__init__()
        self.title("Daftar Alamat")
        self.geometry("600x500")
        self.username = username
        self.account_type = account_type
        self.alamat = alamat
        self.load_user_data()
        self.ensure_user_data()
        
        self.label = tk.Label(self, text="Daftar Alamat", font=("Arial", 18, "bold"))
        self.label.pack(pady=20)
        
        self.address_listbox = tk.Listbox(self, font=("Arial", 12), height=8)
        for address in self.alamat:
            self.address_listbox.insert(tk.END, address)
        self.address_listbox.pack(pady=10, padx=20)
        
        self.add_address_button = tk.Button(self, text="Tambahkan Alamat", font=("Arial", 12), bg="#4caf50", fg="white", command=self.add_address)
        self.add_address_button.pack(pady=5)
        
        self.remove_address_button = tk.Button(self, text="Hilangkan Alamat", font=("Arial", 12), bg="#f44336", fg="white", command=self.remove_address)
        self.remove_address_button.pack(pady=5)
        
        self.set_main_address_button = tk.Button(self, text="Mengatur Alamat Utama", font=("Arial", 12), bg="#2196F3", fg="white", command=self.set_main_address)
        self.set_main_address_button.pack(pady=5)
        
        self.close_button = tk.Button(self, text="Kembali", font=("Arial", 12), bg="#9e9e9e", fg="white", command=self.close_window)
        self.close_button.pack(pady=10)
        
        self.protocol("WM_DELETE_WINDOW", self.close_window)
    
    def add_address(self):
        new_address = simpledialog.askstring("Input", "Masukkan alamat baru:")
        if new_address:
            self.alamat.append(new_address)
            self.update_address_listbox()
            self.save_addresses()
            messagebox.showinfo("Alamat ditambahkan", "Alamat baru sudah ditambahkan!")
    
    def remove_address(self):
        selected_address_index = self.address_listbox.curselection()
        if selected_address_index:
            selected_address = self.address_listbox.get(selected_address_index)
            self.alamat.remove(selected_address)
            self.update_address_listbox()  
            self.save_addresses()
            messagebox.showinfo("Alamat Dihilangkan", f"Alamat '{selected_address}' sudah dihilangkan")
        else:
            messagebox.showwarning("Tidak ada alamat dipilih", "Tolong pilih alamat yang ingin dihilangkan.")
    
    def set_main_address(self):
        selected_address_index = self.address_listbox.curselection()
        if selected_address_index:
            selected_address = self.address_listbox.get(selected_address_index)
            self.alamat.insert(0, self.alamat.pop(self.alamat.index(selected_address)))  
            self.update_address_listbox()  
            self.save_addresses()
            messagebox.showinfo("Alamat Utama Ditetapkan", f"Alamat '{selected_address}' sudah ditetapkan sebagai alamat utama")
        else:
            messagebox.showwarning("Tidak ada alamat yang dipilih", "Tolong pilih alamat untuk ditetapkan sebagai alamat utama.")
    
    def update_address_listbox(self):
        self.address_listbox.delete(0, tk.END)
        for address in self.alamat:
            self.address_listbox.insert(tk.END, address)
    
    def save_addresses(self):
        self.ensure_user_data()
        user_data[self.username]['alamat'] = self.alamat
        self.save_user_data()  

    def close_window(self):
        self.save_addresses() 
        self.destroy()  
        self.settings_window()  
    
    def settings_window(self):
        settings_window = Settings.settings(self.username, self.account_type) 
        self.withdraw()  
        settings_window.deiconify()  
        settings_window.lift()  

    def ensure_user_data(self):
        if self.username not in user_data:
            user_data[self.username] = {
                'basket': [],
                'donasi': [],
                'basket_count': 0,
                'donasi_count': 0,
                'organisasi': "",
                'No. Tlp': "",
                'alamat': []
            }

    def load_user_data(self):
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
        """ Save the current user data to the file """
        with open(user_data_file, "w") as file:
            for username, data in user_data.items():
                basket_count = data['basket_count']
                donasi_count = data['donasi_count']
                organisasi = data['organisasi']
                tlp = data['No. Tlp']
                alamat = ";".join(data['alamat']) 
                file.write(f"{username},{basket_count},{donasi_count},{organisasi},{tlp},{alamat}\n")