import tkinter as tk
from tkinter import simpledialog, messagebox

class Pembayaran(tk.Tk):
    def __init__(self, username, account_type):
        super().__init__()
        self.title("Pembayaran")
        self.geometry("500x400")
        self.configure(bg="#f4f4f4")
        self.username = username
        self.account_type = account_type
        self.user_data = {
            username: {
                'alamat': []
            }
        }
        
        self.alamat = self.user_data[username]['alamat']
        
        self.alamat_label = tk.Label(self, text=f"Alamat Utama: {self.get_main_alamat()}", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#333")
        self.alamat_label.pack(pady=20)
        
        self.alamat_button = tk.Button(self, text="Alamat Pengiriman", font=("Arial", 12), bg="#4caf50", fg="white", command=self.alamat_pengiriman)
        self.alamat_button.pack(pady=10)
        
    def get_main_alamat(self):
        return self.alamat[0] if self.alamat else "Belum ada alamat"
    
    def alamat_pengiriman(self):
        def update_main_alamat():
            selected = listbox.curselection()
            if selected:
                self.alamat_label.config(text=f"Alamat Utama: {self.alamat[selected[0]]}")
                self.user_data[self.username]['alamat'][0] = self.alamat[selected[0]]  
                window.destroy()
            else:
                messagebox.showwarning("Peringatan", "Pilih alamat terlebih dahulu!")
        
        def add_new_alamat():
            new_alamat = simpledialog.askstring("Alamat Baru", "Masukkan alamat baru:")
            if new_alamat:
                self.alamat.append(new_alamat)
                listbox.insert(tk.END, new_alamat)
        
        window = tk.Toplevel(self)
        window.title("Pilih Alamat")
        window.geometry("400x300")

        listbox = tk.Listbox(window, font=("Arial", 12), height=10, width=40)
        listbox.pack(pady=10)

        for alamat in self.alamat:
            listbox.insert(tk.END, alamat)

        if not self.alamat:
            messagebox.showinfo("Info", "Belum ada alamat. Silakan tambahkan yang baru.")

        add_button = tk.Button(window, text="Tambah Alamat", font=("Arial", 12), bg="#4caf50", fg="white", command=add_new_alamat)
        add_button.pack(pady=5)

        select_button = tk.Button(window, text="Pilih Alamat", font=("Arial", 12), bg="#4caf50", fg="white", command=update_main_alamat)
        select_button.pack(pady=5)

if __name__ == "__main__":
    app = Pembayaran("user123", "regular")
    app.mainloop()
