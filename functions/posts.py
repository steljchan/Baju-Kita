import tkinter as tk
from tkinter import simpledialog, messagebox
import os

posts_file = "posts.txt"

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
    try:
        selected_index = self.posts_list.curselection()[0]
        post_details = self.posts_data[selected_index]
        if post_details['creator'] != self.username:
            messagebox.showwarning("Tidak memiliki hak", "Anda hanya bisa mengedit post yang Anda buat.")
            return
        new_nama_post = simpledialog.askstring("Edit Post", f"Edit nama post ({post_details['nama']}):") or post_details['nama']
        new_kategori = simpledialog.askstring("Edit post", f"Edit kategori ({post_details['kategori']}):") or post_details['kategori']
        new_tempat = simpledialog.askstring("Edit Post", f"Edit tempat ({post_details['tempat']}):") or post_details['tempat']
        new_organisasi = simpledialog.askstring("Edit Post", f"Edit organisasi/toko ({post_details['organisasi']}):") or post_details['organisasi']
        new_deskripsi = simpledialog.askstring("Edit Post", f"Edit deskripsi ({post_details['deskripsi']}):") or post_details['deskripsi']
        post_details.update({
            "nama": new_nama_post,
            "kategori": new_kategori,
            "tempat": new_tempat,
            "organisasi": new_organisasi,
            "deskripsi": new_deskripsi
        })
        self.posts_list.delete(selected_index)
        self.posts_list.insert(
            selected_index,
            f"Post: {new_nama_post} | Kategori: {new_kategori} | Tempat: {new_tempat} | Organisasi/Toko: {new_organisasi} | Tipe: {post_details['tipe']} | Deskripsi: {new_deskripsi}"
        )
        with open(posts_file, "w") as file:
            for post in self.posts_data:
                file.write(str(post) + "\n")
        messagebox.showinfo("Post Diedit", "Post berhasil diedit!")
    except IndexError:
        messagebox.showwarning("Tidak ada post yang dipilih", "Tolong pilih post yang ingin diedit.")

def remove_post(self):
    try:
        selected_index = self.posts_listbox.curselection()[0]
        post_details = self.posts_data[selected_index]
        if post_details['creator'] != self.username:
            messagebox.showwarning("Tidak memiliki hak", "Anda hanya bisa menghapus post yang Anda buat.")
            return
        confirmation = messagebox.askyesno("Hapus Post", f"Apakah Anda yakin ingin menghapus post '{post_details['nama']}'?")
        if confirmation:
            self.posts_listbox.delete(selected_index) 
            del self.posts_data[selected_index] 
            with open(posts_file, "w") as file:
                for post in self.posts_data:
                    file.write(str(post) + "\n")
            messagebox.showinfo("Post Dihapus", "Post berhasil dihapus!")
    except IndexError:
        messagebox.showwarning("Tidak ada post yang dipilih", "Tolong pilih post yang ingin dihapus.")
