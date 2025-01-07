import tkinter as tk
from tkinter import messagebox
import Profile
import os
from functions.posts import add_post, edit_post, remove_post

posts_file = "posts.txt"
user_data_file = "user_data.txt"
user_data = {}

class my_posts(tk.Tk):
    def __init__(self, username, account_type):
        tk.Tk.__init__(self)
        self.title("Profile")
        self.geometry("800x700") 
        self.configure(bg="#f4f4f4")
        self.username = username
        self.account_type = account_type
        self.posts_data = []
        self.load_posts()
        self.label_title = tk.Label(
            self, text=f"Posts by {self.username}", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#333"
        )
        self.label_title.pack(pady=20)
        self.posts_listbox = tk.Listbox(self, font=("Arial", 12), width=80, height=20)
        self.posts_listbox.pack(pady=10)
        self.show_my_posts()
        self.add_post_button = tk.Button(
            self, text="Add Post", font=("Arial", 12), bg="#4caf50", fg="white", command=self.add_post
        )
        self.add_post_button.pack(pady=10)
        
        self.edit_post_button = tk.Button(
            self, text="Edit Post", font=("Arial", 12), bg="#00008B", fg="white", command=self.edit_post
        )
        self.edit_post_button.pack(pady=10)
        self.close_button = tk.Button(
            self, text="Kembali", font=("Arial", 12), bg="#ff6f61", fg="white", command=self.back
        )
        self.remove_post_button = tk.Button(
            self, text="Remove Post", font=("Arial", 12), bg="#f44336", fg="white", command=self.remove_post
        )
        self.remove_post_button.pack(pady=10)
        self.close_button.place(x=600, y=20)
    
    def load_posts(self):
        try:
            if os.path.exists(posts_file):
                with open(posts_file, "r") as file:
                    posts_list_data = file.readlines()
                    for post in posts_list_data:
                        post_dict = eval(post.strip())  
                        if isinstance(post_dict, dict):
                            self.posts_data.append(post_dict)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading posts: {e}")
    
    def show_my_posts(self):
        self.posts_listbox.delete(0, tk.END)  
        for post in self.posts_data:
            if post.get("creator", "") == self.username:
                display_post = (
                    f"Post: {post['nama']} | Tempat: {post['tempat']} | "
                    f"Organisasi: {post['organisasi']} | Tipe: {post['tipe']} | "
                    f"Deskripsi: {post['deskripsi']}"
                )
                self.posts_listbox.insert(tk.END, display_post)
    
    def add_post(self):
        add_post(self) 
    
    def edit_post(self):
        edit_post(self)  
    
    def remove_post(self):
        remove_post(self)
    
    def back(self):
        self.destroy()  
        self.profile_window()  
    
    def profile_window(self):
        profile_window = Profile.profile(self.username, self.account_type) 
        self.withdraw()  
        profile_window.deiconify()  
        profile_window.lift()  

if __name__ == "__main__":
    app = my_posts(username="User1", account_type="penjual")
    app.mainloop()
