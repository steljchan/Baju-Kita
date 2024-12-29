import tkinter as tk
from tkinter import messagebox
import os
import re

USER_FILE = "users.txt"
GOOGLE_ACCOUNTS = [
    {"username": "google_user1", "account_type": "customer"},
    {"username": "google_user2", "account_type": "seller"},
    {"username": "google_user3", "account_type": "customer"}
]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Masuk / Daftar")
        self.geometry("400x400")

        # Nama Aplikasi
        self.label_title = tk.Label(self, text="Baju Kita", font=("Helvetica", 20))
        self.label_title.pack(pady=10)

        # Input username dan password
        self.label_username = tk.Label(self, text="Nama Pengguna:")
        self.label_username.pack(pady=5)
        self.entry_username = tk.Entry(self, width=30)
        self.entry_username.pack(pady=5)

        self.label_password = tk.Label(self, text="Kata Sandi:")
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(self, width=30, show="*")
        self.entry_password.pack(pady=5)

        # Button Sign In
        self.button_sign_in = tk.Button(self, text="Masuk", width=15, command=self.sign_in)
        self.button_sign_in.pack(pady=5)

        # Button Register
        self.button_register = tk.Button(self, text="Belum memiliki akun? Daftar disini", fg="blue", underline=True, command=self.register_user)
        self.button_register.pack(pady=5)

        # Button Google Sign In
        self.button_google_sign_in = tk.Button(self, text="Masuk dengan Google", width=20, command=self.google_sign_in)
        self.button_google_sign_in.pack(pady=5)

        self.create_user_file()

        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def create_user_file(self):
        if not os.path.exists(USER_FILE):
            with open(USER_FILE, "w") as file:
                pass

    def clear_widgets(self):
        """Utility function to clear all widgets from the window."""
        for widget in self.winfo_children():
            widget.pack_forget()

    def register_user(self):
        self.clear_widgets()

        # Registration form
        self.label_title.pack(pady=10)
        self.label_username.config(text="Nama Pengguna Baru:")
        self.label_username.pack(pady=5)
        self.entry_username.pack(pady=5)

        self.label_password.config(text="Kata Sandi Baru:")
        self.label_password.pack(pady=5)
        self.entry_password.pack(pady=5)

        self.label_confirm_password = tk.Label(self, text="Konfirmasi Kata Sandi:")
        self.label_confirm_password.pack(pady=5)
        self.entry_confirm_password = tk.Entry(self, width=30, show="*")
        self.entry_confirm_password.pack(pady=5)

        self.label_account_type = tk.Label(self, text="Tipe Akun")
        self.label_account_type.pack(pady=5)
        self.account_type_var = tk.StringVar(value="customer")
        tk.Radiobutton(self, text="Pelanggan", variable=self.account_type_var, value="customer").pack(pady=5)
        tk.Radiobutton(self, text="Penjual", variable=self.account_type_var, value="seller").pack(pady=5)

        tk.Button(self, text="Daftar", width=15, command=self.save_user).pack(pady=5)
        tk.Button(self, text="Kembali ke Halaman Masuk", width=20, command=self.reset_to_sign_in).pack(pady=5)

    def reset_to_sign_in(self):
        self.clear_widgets()
        self.show_sign_in_page()

    def save_user(self):
        new_username = self.entry_username.get()
        new_password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()
        account_type = self.account_type_var.get()

        if new_password != confirm_password:
            messagebox.showerror("Eror", "Kata sandi dan konfirmasi kata sandi tidak cocok.")
            return

        if not self.validate_password(new_password):
            messagebox.showerror("Eror", "Kata sandi harus memiliki minimal 6 karakter dan mengandung angka.")
            return

        if self.username_exists(new_username):
            messagebox.showerror("Eror", "Nama pengguna sudah ada.")
            return

        with open(USER_FILE, "a") as file:
            file.write(f"{new_username},{new_password},{account_type}\n")
        messagebox.showinfo("Berhasil", "Pendaftaran Berhasil!")
        self.reset_to_sign_in()

    def validate_password(self, password):
        return len(password) >= 6 and re.search(r'\d', password)

    def username_exists(self, username):
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r") as file:
                users = file.readlines()
                for user in users:
                    if username == user.strip().split(",")[0]:
                        return True
        return False

    def sign_in(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username and password:
            if os.path.exists(USER_FILE):
                with open(USER_FILE, "r") as file:
                    users = file.readlines()
                    for user in users:
                        # Split and validate the line
                        values = user.strip().split(",")
                        if len(values) != 3:
                            # Skip malformed lines
                            continue

                        saved_username, saved_password, saved_account_type = values
                        if username == saved_username and password == saved_password:
                            self.show_homepage(saved_username, saved_account_type)
                            return
            messagebox.showerror("Eror", "Nama pengguna atau kata sandi salah.")
        else:
            messagebox.showerror("Eror", "Masukkan nama pengguna dan kata sandi.")

    def google_sign_in(self):
        self.clear_widgets()

        self.label_title.pack(pady=10)
        self.label_select_account = tk.Label(self, text="Pilih Akun Google", font=("Helvetica", 20))
        self.label_select_account.pack(pady=10)

        self.google_account_var = tk.StringVar(value=GOOGLE_ACCOUNTS[0]["username"])
        for account in GOOGLE_ACCOUNTS:
            tk.Radiobutton(self, text=account["username"], variable=self.google_account_var, value=account["username"]).pack(pady=5)

        tk.Button(self, text="Pilih", width=15, command=self.select_google_account).pack(pady=5)
        tk.Button(self, text="Kembali ke Halaman Masuk", width=20, command=self.reset_to_sign_in).pack(pady=5)

    def select_google_account(self):
        selected_username = self.google_account_var.get()
        for account in GOOGLE_ACCOUNTS:
            if account["username"] == selected_username:
                self.show_homepage(account["username"], account["account_type"])
                return

    def show_homepage(self, username, account_type):
        self.clear_widgets()
        self.label_title.pack(pady=10)
        self.label_welcome = tk.Label(self, text=f"Selamat datang, {username}!", font=("Helvetica", 20))
        self.label_welcome.pack(pady=10)
        tk.Button(self, text="Keluar", width=15, command=self.logout).pack(pady=5)

    def logout(self):
    # Clear username and password
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

        # Kembali ke sign-in page
        self.reset_to_sign_in()


    def show_sign_in_page(self):
        self.clear_widgets()
        self.label_title.pack(pady=10)
        self.label_username.pack(pady=5)
        self.entry_username.pack(pady=5)
        self.label_password.pack(pady=5)
        self.entry_password.pack(pady=5)
        self.button_sign_in.pack(pady=5)
        self.button_register.pack(pady=5)
        self.button_google_sign_in.pack(pady=5)

    def on_exit(self):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
