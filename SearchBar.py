import tkinter as tk
from tkinter import messagebox
import Homepage  # Import Homepage to navigate back
import Profile  # Import Profile page

class SearchPage(tk.Tk):
    def __init__(self, username, account_type):
        super().__init__()
        self.title("Search Page")
        self.geometry("800x600")
        self.configure(bg="#f4f4f4")
        self.username = username
        self.account_type = account_type
        
        # Header (Welcome message)
        self.label_welcome = tk.Label(self, text=f"Search Thrift Items, {self.username}", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#333")
        self.label_welcome.pack(pady=20)
        
        # Search Bar
        self.search_entry = tk.Entry(self, width=40, font=("Arial", 12))
        self.search_entry.pack(pady=5)

        # Search Button
        search_button = tk.Button(self, text="Search", font=("Arial", 12), command=self.search_items)
        search_button.pack(pady=5)

        # Result Listbox
        self.result_list = tk.Listbox(self, width=60, height=10, font=("Arial", 12))
        self.result_list.pack(pady=10)

        # Bottom Navigation Bar with four buttons
        self.nav_bar = tk.Frame(self, bg="#dddddd", height=50)
        self.nav_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Button for Homepage
        home_button = tk.Button(self.nav_bar, text="Homepage", font=("Arial", 12), bg="#007BFF", fg="white", command=self.go_to_homepage)
        home_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Button for Searchpage (Disable when on SearchPage)
        search_button = tk.Button(self.nav_bar, text="Search Page", font=("Arial", 12), bg="#6c757d", fg="white", command=self.go_to_searchpage)
        search_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Button for Donation Page
        donation_button = tk.Button(self.nav_bar, text="Donation Page", font=("Arial", 12), bg="#28a745", fg="white", command=self.go_to_donasi)
        donation_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Button for Profile
        profile_button = tk.Button(self.nav_bar, text="Profile", font=("Arial", 12), bg="#ffc107", fg="white", command=self.go_to_profile)
        profile_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def search_items(self):
        query = self.search_entry.get()
        if not query:
            messagebox.showwarning("Search Error", "Please enter a keyword to search.")
            return

        # Read posts from the file and filter by the search query
        posts = self.load_posts()
        matching_posts = [post for post in posts if query.lower() in post.lower()]
        
        if not matching_posts:
            messagebox.showinfo("No Results", "No matching posts found.")
        
        self.display_results(matching_posts)

    def load_posts(self):
        # Load posts from the "posts.txt" file
        try:
            with open("posts.txt", "r") as file:
                posts = file.readlines()
            return [post.strip() for post in posts]  # Remove leading/trailing whitespaces
        except FileNotFoundError:
            messagebox.showerror("Error", "Posts file not found.")
            return []

    def display_results(self, results):
        self.result_list.delete(0, tk.END)  # Clear previous results
        for result in results:
            self.result_list.insert(tk.END, result)

    def go_to_homepage(self):
        self.destroy()
        app = Homepage.Homepage(username=self.username, account_type=self.account_type)
        app.mainloop()

    def go_to_searchpage(self):
        messagebox.showinfo("Search Page", "You are already on the Search Page.")
    
    def go_to_donasi(self):
        self.destroy()

    def go_to_profile(self):
        self.destroy()
        profile_app = Profile.profile(username=self.username, account_type=self.account_type)
        profile_app.mainloop()

if __name__ == "__main__":
    app = SearchPage(username="Seller1", account_type="penjual")
    app.mainloop()
