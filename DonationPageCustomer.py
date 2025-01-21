import tkinter as tk
from tkinter import messagebox
import Homepage
import SearchBar
import Profile

class DonationPageCus(tk.Tk):
    def __init__(self, username, account_type):
        super().__init__()
        self.title("BajuKita - Donation Page")
        self.geometry("500x600")
        self.eval('tk::PlaceWindow . center')
        self.username = username
        self.account_type = account_type

        self.donation_events = [
            {"name": "Donation Event 1", "description": "Description for Donation Event 1"},
            {"name": "Donation Event 2", "description": "Description for Donation Event 2"},
            {"name": "Donation Event 3", "description": "Description for Donation Event 3"},
        ]

        self.pages = {}
        self.create_pages()
        self.create_navigation_buttons()

    def create_pages(self):
        self.pages["home"] = tk.Frame(self, bg="#f5f5f5")
        self.pages["home"].pack(fill=tk.BOTH, expand=True)
        self.pages["home"].tkraise()

        self.pages["donation"] = tk.Frame(self, bg="#fff3e0")
        self.pages["donation"].pack(fill=tk.BOTH, expand=True)

        self.pages["profile"] = tk.Frame(self, bg="#e1bee7")
        self.pages["profile"].pack(fill=tk.BOTH, expand=True)

        self.pages["search"] = tk.Frame(self, bg="#c8e6c9")
        self.pages["search"].pack(fill=tk.BOTH, expand=True)

        self.create_home_page()
        self.create_donation_page()

    def create_home_page(self):
        label_title = tk.Label(self.pages["home"], text="Welcome to BajuKita", font=("Helvetica", 20, "bold"), bg="#f5f5f5", fg="#00796b")
        label_title.pack(pady=20)

    def create_donation_page(self):
        label_title = tk.Label(self.pages["donation"], text="Donation Events", font=("Helvetica", 15), bg="#fff3e0", fg="#d32f2f")
        label_title.pack(pady=20)

        self.donation_frame_donation = tk.Frame(self.pages["donation"], bg="#fff3e0")
        self.donation_frame_donation.pack(pady=10, fill=tk.X)
        self.create_donation_buttons_donation()

    def create_donation_buttons_donation(self):
        for widget in self.donation_frame_donation.winfo_children():
            widget.destroy()
        for event in self.donation_events:
            button = tk.Button(self.donation_frame_donation, text=event["name"], command=lambda e=event: self.show_event_description(e), font=("Helvetica", 12), bg="#8e24aa", fg="white", relief="solid")
            button.pack(pady=10, fill=tk.X, padx=20)

    def show_event_description(self, event):
        description_window = tk.Toplevel(self)
        description_window.title(event["name"])
        description_window.geometry("400x300")

        label_name = tk.Label(description_window, text=event["name"], font=("Helvetica", 16, "bold"))
        label_name.pack(pady=10)

        text_description = tk.Text(description_window, wrap=tk.WORD, font=("Helvetica", 12), height=6)
        text_description.insert(tk.END, event["description"])
        text_description.config(state=tk.DISABLED)
        text_description.pack(pady=10, padx=20)

        join_button = tk.Button(description_window, text="Join Event", command=lambda: self.join_donation_event(event["name"]), font=("Helvetica", 12), bg="#0288d1", fg="white")
        join_button.pack(pady=10)

    def join_donation_event(self, event):
        messagebox.showinfo("Join Donation Event", f"You have joined {event}!")

    def create_navigation_buttons(self):
        nav_frame = tk.Frame(self, bg="#00796b")
        nav_frame.pack(side=tk.BOTTOM, fill=tk.X)

        home_button = tk.Button(nav_frame, text="Home", command=lambda: self.show_page("home"), font=("Helvetica", 12), bg="#004d40", fg="white")
        home_button.pack(side=tk.LEFT, expand=True, fill=tk.X)

        search_button = tk.Button(nav_frame, text="Search", command=lambda: self.go_to_searchpage(), font=("Helvetica", 12), bg="#388e3c", fg="white")
        search_button.pack(side=tk.LEFT, expand=True, fill=tk.X)

        donation_button = tk.Button(nav_frame, text="Donation", command=lambda: self.show_page("donation"), font=("Helvetica", 12), bg="#d32f2f", fg="white")
        donation_button.pack(side=tk.LEFT, expand=True, fill=tk.X)

        profile_button = tk.Button(nav_frame, text="Profile", command=lambda: self.go_to_profile(), font=("Helvetica", 12), bg="#fbc02d", fg="white")
        profile_button.pack(side=tk.LEFT, expand=True, fill=tk.X)

    def show_page(self, page):
        self.pages[page].tkraise()

    def go_to_homepage(self):
        self.destroy()
        homepage_app = Homepage.Homepage(username=self.username, account_type=self.account_type)
        homepage_app.mainloop()

    def go_to_searchpage(self):
        self.destroy()
        search_app = SearchBar.SearchPage(username=self.username, account_type=self.account_type)
        search_app.mainloop()

    def go_to_profile(self):
        self.destroy()
        profile_app = Profile.profile(username=self.username, account_type=self.account_type)
        profile_app.mainloop()

if __name__ == "__main__":
    app = DonationPageCus(username="Customer1", account_type="customer")
    app.mainloop()
