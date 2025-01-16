import tkinter as tk
from tkinter import simpledialog, messagebox
import os

posts_file = "posts.txt"
basket_file = "basket.txt"
donasi_file = "donasi.txt"

def add_post(self):
    nama_post = simpledialog.askstring("Input", "Masukkan nama post: ")
    while True:
        kategori = simpledialog.askstring("Input", "Masukkan kategori baju (bayi, balita, anak-anak, remaja, dewasa):")
        if kategori and kategori.lower() in ['bayi', 'balita', 'anak-anak', 'remaja', 'dewasa']:
            break
        else:
            messagebox.showwarning("Kategori salah", "Kategori harus 'bayi', 'balita', 'anak-anak', 'remaja', atau 'dewasa'.")
    while True:
        tipe_post = simpledialog.askstring("Input", "Masukkan tipe post (Thrift atau Donasi): ")
        if tipe_post and tipe_post.lower() in ["thrift", "donasi"]:
            break
        else:
            messagebox.showwarning("Tipe post salah", "Tipe post harus 'Thrift' atau 'Donasi'.")
    if tipe_post.lower() == "thrift":
        tempat = simpledialog.askstring("Input", "Masukkan tempat (Nama kota): ")
        organisasi = simpledialog.askstring("Input", "Masukkan nama toko: ")
        deskripsi = simpledialog.askstring("Input", "Masukkan deskripsi (Jenis baju, Jenis kain, Harga baju): ")
    else:
        tempat = simpledialog.askstring("Input", "Masukkan tempat (Nama jalan, Nama kota): ")
        organisasi = simpledialog.askstring("Input", "Masukkan nama organisasi: ")
        deskripsi = simpledialog.askstring("Input", "Masukkan deskripsi (Jenis baju yang dibutuhkan, Jenis kain yang diinginkan, tujuan donasi): ")
    if not nama_post or not tempat or not organisasi or not tipe_post or not deskripsi:
        messagebox.showwarning("Informasi post tidak lengkap", "Tolong isi semua informasi (nama, tempat, organisasi, tipe, dan deskripsi).")
        return
    post_details = {
        "nama": nama_post,
        "kategori": kategori,
        "tempat": tempat,
        "organisasi": organisasi,
        "tipe": tipe_post,
        "deskripsi": deskripsi,
        "creator": self.username
    }
    self.posts_listbox.insert(
        tk.END,
        f"Post: {nama_post} | Kategori: {kategori} | Tempat: {tempat} | Organisasi/Toko: {organisasi} | Tipe: {tipe_post} | Deskripsi: {deskripsi}"
    )
    with open(posts_file, "a") as file:
        file.write(str(post_details) + "\n")
    messagebox.showinfo("Post Ditambahkan", f"Post '{nama_post}' telah berhasil ditambahkan!")

def edit_post(self):
    if not hasattr(self, 'posts_listbox'):
        messagebox.showerror("Error", "No posts list found.")
        return
    try:
        selected_index = self.posts_listbox.curselection()[0]
        post_details = self.posts_data[selected_index]
        tipe_post = post_details['tipe'].lower()
        organisasi = post_details['organisasi']
        if post_details['creator'] != self.username:
            messagebox.showwarning("Permission Denied", "You can only edit posts you created.")
            return
        if post_details['creator'] != self.username:
            messagebox.showwarning("Tidak memiliki hak", "Anda hanya bisa mengedit post yang Anda buat.")
            return
        new_nama_post = simpledialog.askstring("Edit Post", f"Edit nama post ({post_details['nama']}):") or post_details['nama']
        new_kategori = simpledialog.askstring("Edit post", f"Edit kategori ({post_details['kategori']}):") or post_details['kategori']
        new_tempat = simpledialog.askstring("Edit Post", f"Edit tempat ({post_details['tempat']}):") or post_details['tempat']
        if tipe_post == "thrift":
            new_harga = simpledialog.askstring("Edit Post", "Edit harga baju:") or post_details.get("harga", "")
            new_deskripsi = simpledialog.askstring("Edit Post", f"Edit deskripsi ({post_details['deskripsi']}):") or post_details['deskripsi']
            post_details.update({
                "nama": new_nama_post,
                "kategori": new_kategori,
                "tempat": new_tempat,
                "harga": new_harga,
                "deskripsi": new_deskripsi
            })
            display_text = (
                f"Post: {new_nama_post} | Kategori: {new_kategori} | Tempat: {new_tempat} | "
                f"Organisasi/Toko: {organisasi} | Tipe: {post_details['tipe']} | "
                f"Harga: {new_harga} | Deskripsi: {new_deskripsi}"
            )
        elif tipe_post == "donasi":
            new_jumlah_baju = simpledialog.askstring("Edit Post", "Edit baju yang dibutuhkan:") or post_details.get("baju_dibutuhkan", "")
            post_details.update({"baju_dibutuhkan": new_jumlah_baju})
            new_deskripsi = simpledialog.askstring("Edit Post", f"Edit deskripsi ({post_details['deskripsi']}):") or post_details['deskripsi']
            post_details.update({
                "nama": new_nama_post,
                "kategori": new_kategori,
                "tempat": new_tempat,
                "deskripsi": new_deskripsi,
                "jumlah_baju": new_jumlah_baju
            })
            display_text = (
                f"Post: {new_nama_post} | Kategori: {new_kategori} | Tempat: {new_tempat} | "
                f"Organisasi/Toko: {organisasi} | Tipe: {post_details['tipe']} | "
                f"Deskripsi: {new_deskripsi} | Baju Dibutuhkan: {new_jumlah_baju}"
            )
        else:
            messagebox.showerror("Error", "Unknown post type.")
            return
        self.posts_listbox.delete(selected_index)
        self.posts_listbox.insert(selected_index, display_text)
        with open(posts_file, "w") as file:
            for post in self.posts_data:
                file.write(str(post) + "\n")
        messagebox.showinfo("Post Diedit", "Post berhasil diedit!")
    except IndexError:
        messagebox.showwarning("Tidak ada post yang dipilih", "Tolong pilih post yang ingin diedit.")
        return

def remove_post(self):
    try:
        selected_index = self.posts_listbox.curselection()[0]
        post_details = self.posts_data[selected_index]
        if post_details['creator'] != self.username:
            messagebox.showwarning("Tidak memiliki hak", "Anda hanya bisa menghapus post yang Anda buat.")
            return
        confirmation = messagebox.askyesno("Hapus Post", f"Apakah Anda yakin ingin menghapus post '{post_details['nama']}'?")
        if confirmation:
            if post_details['tipe'].lower() == "thrift":
                self.remove_from_basket(post_details)
            elif post_details['tipe'].lower() == "donasi":
                self.remove_from_donasi(post_details)
            else:
                messagebox.showerror("Error", "Unknown post type.")
                return
            self.posts_listbox.delete(selected_index)
            del self.posts_data[selected_index]
            with open(posts_file, "w") as file:
                for post in self.posts_data:
                    file.write(str(post) + "\n")
            
            messagebox.showinfo("Post Dihapus", "Post berhasil dihapus!")
    except IndexError:
        messagebox.showwarning("Tidak ada post yang dipilih", "Tolong pilih post yang ingin dihapus.")

def remove_from_basket(self, post_details):
    try:
        with open(basket_file, "r") as file:
            lines = file.readlines()
        updated_lines = []
        for line in lines:
            username, item = line.strip().split(",", 1)
            if item == post_details['nama'] and username == self.username:
                continue  
            updated_lines.append(line)
        with open(basket_file, "w") as file:
            file.writelines(updated_lines)
        if self.username in self.user_data:
            self.user_data[self.username]['basket_count'] = max(0, self.user_data[self.username]['basket_count'] - 1)
            self.save_user_data()
    except Exception as e:
        print(f"Error removing from basket: {e}")

def remove_from_donasi(self, post_details):
    try:
        with open(donasi_file, "r") as file:
            lines = file.readlines()
        updated_lines = []
        for line in lines:
            username, item = line.strip().split(",", 1)
            if item == post_details['nama'] and username == self.username:
                continue  
            updated_lines.append(line)
        with open(donasi_file, "w") as file:
            file.writelines(updated_lines)
        if self.username in self.user_data:
            self.user_data[self.username]['donasi_count'] = max(0, self.user_data[self.username]['donasi_count'] - 1)
            self.save_user_data()
    except Exception as e:
        print(f"Error removing from donasi: {e}")