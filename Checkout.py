import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import Homepage
import Payment

basket_file = "basket.txt"
user_data_file = "user_data.txt"
orderan_file = "orderan.txt"
user_data = {}

class pembayaran(tk.Tk):
    def __init__(self, username, account_type):
        tk.Tk.__init__(self)
        self.title("Pembayaran")
        self.geometry("600x550") 
        self.configure(bg="#f4f4f4")
        self.ensure_file_exists()
        self.load_user_data()
        self.username = username
        self.account_type = account_type
        self.payment_method = None
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
        self.alamat = self.user_info['alamat']
        
        self.alamat_label = tk.Label(self, text=f"Alamat Utama: {self.get_main_alamat()}", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#333")
        self.alamat_label.pack(pady=20)
        
        self.alamat_button = tk.Button(self, text="Pilih Alamat", font=("Arial", 12), bg="#4caf50", fg="white", command=self.alamat_pengiriman)
        self.alamat_button.pack(pady=10)
        
        self.basket_list = tk.Listbox(self, font=("Arial", 12), height=8, width=50)
        self.basket_list.pack(pady=10)
        
        self.pengiriman_label = tk.Label(self, text=f"Metode Pengiriman: {self.get_pengiriman()}", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#333")
        self.pengiriman_label.pack(pady=20)
        
        self.pengiriman_button = tk.Button(self, text="Pilih Metode Pengiriman", font=("Arial", 12), bg="#4caf50", fg="white", command=self.pengiriman)
        self.pengiriman_button.pack(pady=10)

        self.pembayaran_button = tk.Button(self, text="Lanjut Pembayaran", font=("Arial", 12), bg="#4caf50", fg="white", command=self.pembayaran)
        self.pembayaran_button.pack(pady=10) 
        
        self.cancel_button = tk.Button(self, text="Batal", font=("Arial", 12), bg="#4caf50", fg="white", command=self.homepage)
        self.cancel_button.pack(pady=10)
        
        self.load_basket()

    def ensure_file_exists(self):
        if not os.path.exists(basket_file):
            open(basket_file, "w").close()

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

    def get_main_alamat(self):
        return self.alamat[0] if self.alamat else "Belum ada alamat"

    def alamat_pengiriman(self):
        def update_main_alamat():
            selected = listbox.curselection()
            if selected:
                self.alamat_label.config(text=f"Alamat Utama: {self.alamat[selected[0]]}")
                self.user_info['alamat'][0] = self.alamat[selected[0]]
                print(f"Updated main address: {self.alamat[selected[0]]}")
                self.save_addresses()
                window.destroy()
            else:
                messagebox.showwarning("Peringatan", "Pilih alamat terlebih dahulu!")
        def add_new_alamat():
            new_address = simpledialog.askstring("Input", "Masukkan alamat baru (Nama-No. Tlp-Kota-Kecamatan-Kelurahan-Kode Pos-Jalan):")
            if new_address:
                self.alamat.append(new_address)
                self.update_address_listbox(listbox)
                self.save_addresses()
                messagebox.showinfo("Alamat Ditambahkan", "Alamat baru telah ditambahkan!")
        window = tk.Toplevel(self)
        window.title("Pilih Alamat")
        window.geometry("400x300")
        
        listbox = tk.Listbox(window, font=("Arial", 12), height=10, width=40)
        listbox.pack(pady=10)
        self.update_address_listbox(listbox)
        
        add_button = tk.Button(window, text="Tambah Alamat", font=("Arial", 12), bg="#4caf50", fg="white", command=add_new_alamat)
        add_button.pack(pady=5)
        
        select_button = tk.Button(window, text="Pilih Alamat", font=("Arial", 12), bg="#4caf50", fg="white", command=update_main_alamat)
        select_button.pack(pady=5)

    def load_basket(self):
        self.basket_list.delete(0, tk.END)
        if os.path.exists(basket_file):
            try:
                with open(basket_file, "r") as f:
                    for line in f:
                        if line.strip():
                            try:
                                username, basket_data = line.split(",", 1)
                                if username.strip() == self.username:
                                    item = eval(basket_data.strip())  
                                    display_text = f"{item['nama']} - {item['creator']} - {item['harga']}"
                                    self.basket_list.insert(tk.END, display_text)
                            except (ValueError, SyntaxError) as e:
                                print(f"Error parsing basket item: {line.strip()} ({e})")
            except Exception as e:
                print(f"Error reading {basket_file}: {e}")

    def get_pengiriman(self):
        return "Belum ada metode"

    def pengiriman(self):
        def select_pengiriman():
            selected_method = method_var.get()
            if selected_method:
                self.pengiriman_label.config(text=f"Metode Pengiriman: {selected_method}")
                window.destroy()
            else:
                messagebox.showwarning("Peringatan", "Pilih metode pengiriman terlebih dahulu!")
        methods = ["Reguler", "Express", "Same Day", "Pick Up"]
        window = tk.Toplevel(self)
        window.title("Pilih Metode Pengiriman")
        window.geometry("400x300")
        method_var = tk.StringVar(value="") 
        
        for method in methods:
            radio_button = tk.Radiobutton(window, text=method, variable=method_var, value=method, font=("Arial", 12), bg="#f4f4f4", fg="#333")
            radio_button.pack(pady=5)
        
        select_button = tk.Button(window, text="Pilih Metode", font=("Arial", 12), bg="#4caf50", fg="white", command=select_pengiriman)
        select_button.pack(pady=10)
    
    def pembayaran(self):
        main_address = self.get_main_alamat()
        if main_address == "Belum ada alamat":
            messagebox.showwarning("Peringatan", "Alamat belum dipilih!")
            return
        pengiriman_method = self.pengiriman_label.cget("text").replace("Metode Pengiriman: ", "")
        if pengiriman_method == "Belum ada metode":
            messagebox.showwarning("Peringatan", "Metode pengiriman belum dipilih!")
            return
        shipping_costs = {
            "Reguler": 7000,
            "Express": 20000,
            "Same Day": 40000,
            "Pick Up": 0
        }
        shipping_cost = shipping_costs.get(pengiriman_method, 0)
        basket_items = self.basket_list.get(0, tk.END)
        if not basket_items:
            messagebox.showwarning("Peringatan", "Keranjang belanja kosong!")
            return
        total_price = 0
        try:
            with open(orderan_file, "a") as file:
                for item_display in basket_items:
                    try:
                        nama, creator, harga = item_display.split(" - ")
                        harga = int(harga.replace(".", "").replace(",", ""))  
                        file.write(f"{self.username},{nama},{creator},{harga},{main_address},{pengiriman_method},belum dibayar\n")
                        total_price += harga
                    except ValueError:
                        messagebox.showerror("Error", f"Format keranjang tidak valid: {item_display}")
                        continue
            total_price += shipping_cost
            messagebox.showinfo("Sukses", f"Pesanan telah disimpan dengan status 'belum dibayar'. Total harga: Rp{total_price:,}")
            self.basket_list.delete(0, tk.END)
            self.user_info['basket_count'] = 0
            self.save_user_data()
            with open(basket_file, "w") as f:
                pass
            self.open_payment_window(total_price)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan pesanan: {e}")
    
    def homepage(self):
        self.destroy()
        Homepage.Homepage(self.username, self.account_type).mainloop()

    def save_user_data(self):
        try:
            with open(user_data_file, "r") as file:
                lines = file.readlines()
            with open(user_data_file, "w") as file:
                for line in lines:
                    parts = line.strip().split(',')
                    if parts[0] == self.username:
                        parts[1] = str(self.user_info['basket_count'])
                    file.write(",".join(parts) + "\n")
        except Exception as e:
            print(f"Error saving user data: {e}")
            messagebox.showerror("Error", "Gagal menyimpan data pengguna!")

    def update_address_listbox(self, listbox):
        listbox.delete(0, tk.END)
        for alamat in self.alamat:
            listbox.insert(tk.END, alamat)

    def save_addresses(self):
        try:
            with open(user_data_file, "r") as file:
                lines = file.readlines()
            with open(user_data_file, "w") as file:
                for line in lines:
                    parts = line.strip().split(',')
                    if parts[0] == self.username:
                        parts[7] = ";".join(self.alamat)
                    file.write(",".join(parts) + "\n")
        except Exception as e:
            print(f"Error saving addresses: {e}")
            messagebox.showerror("Error", "Gagal menyimpan alamat!")

    def homepage(self):
        self.destroy()
        Homepage.Homepage(self.username, self.account_type).mainloop()
    
    def open_payment_window(self, total_price):
        self.destroy()  
        Payment.selesai(self.username, total_price).mainloop()  
