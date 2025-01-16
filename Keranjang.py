import tkinter as tk
from tkinter import messagebox
import Homepage
import Checkout
import os

posts_file = "posts.txt"
user_data_file = "user_data.txt"
basket_file = "basket.txt"
orderan_file = "orderan.txt"
user_data = {}

class basket(tk.Tk):
    def __init__(self, username, account_type):
        tk.Tk.__init__(self)
        self.title("Keranjang Anda")
        self.geometry("600x450")
        self.configure(bg="#f4f4f4")
        self.ensure_file_exists()
        self.username = username
        self.account_type = account_type
        self.load_user_data()
        
        self.label_keranjang = tk.Label(self, text="Keranjang Anda", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#333")
        self.label_keranjang.pack(pady=20)
        
        self.basket_list = tk.Listbox(self, font=("Arial", 12), height=8, width=50)
        self.basket_list.pack(pady=10)
        
        self.remove_button = tk.Button(self, text="Hilangkan", font=("Arial", 12), bg="#4caf50", fg="white", command=self.remove)
        self.remove_button.pack(pady=10)
        
        self.checkout_button = tk.Button(self, text="Bayar Sekarang", font=("Arial", 12), bg="#4caf50", fg="white", command=self.checkout)
        self.checkout_button.pack(pady=10)
        
        self.back_button = tk.Button(self, text="Kembali", font=("Arial", 12), bg="#4caf50", fg="white", command=self.homepage)
        self.back_button.pack(pady=10)
        
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
                        if len(parts) < 7:
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
    
    def load_basket(self):
        self.basket_list.delete(0, tk.END) 
        print(f"Loading basket for user: {self.username}") 
        if os.path.exists(basket_file):
            with open(basket_file, "r") as f:
                for line in f:
                    if line.strip(): 
                        try:
                            username, post_data = line.split(",", 1)
                            print(f"Read line - Username: {username}, Post Data: {post_data}")
                            if username.strip() == self.username: 
                                self.basket_list.insert(tk.END, post_data.strip())
                        except ValueError:
                            print(f"Line format error: {line.strip()}")  
    
    def save_basket(self):
        if os.path.exists(basket_file):
            with open(basket_file, "r") as f:
                lines = f.readlines()
        with open(basket_file, "w") as f:
            for line in lines:
                if not line.startswith(f"{self.username},"):
                    f.write(line)
            for i in range(self.basket_list.size()):
                post_data = self.basket_list.get(i)
                f.write(f"{self.username},{post_data}\n")
    
    def remove(self):
        try:
            selected_index = self.basket_list.curselection()[0] 
            selected_item = self.basket_list.get(selected_index)
            self.basket_list.delete(selected_index)  
            if os.path.exists(basket_file):
                with open(basket_file, "r") as f:
                    lines = f.readlines()
                with open(basket_file, "w") as f:
                    for line in lines:
                        if line.strip() != f"{self.username},{selected_item}":
                            f.write(line)
            if self.username in user_data:
                user_data[self.username]['basket_count'] -= 1
                if user_data[self.username]['basket_count'] < 0:
                    user_data[self.username]['basket_count'] = 0 
                self.save_user_data()
            messagebox.showinfo("Item Removed", "Item has been removed from your basket.")
        except IndexError:
            messagebox.showwarning("No Selection", "Please select an item to remove.")
    
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
    
    def checkout(self):
        if self.basket_list.size() == 0:
            messagebox.showinfo("Checkout", "Your basket is empty!")
            return
        self.save_basket() 
        self.destroy()  
        Checkout.pembayaran(self.username, self.account_type).mainloop()  
    
    def homepage(self):
        self.destroy()
        Homepage.Homepage(self.username, self.account_type).mainloop()

if __name__ == "__main__":
    app = basket(username="User1", account_type="pembeli")
    app.mainloop()
