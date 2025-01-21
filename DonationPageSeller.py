import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from BiodataPenyelenggaraDonasi import Biodata_Penyelenggara

class DonationPageSell(tk.Tk):
    def __init__(self, username, account_type):
        super().__init__()
        self.title("Donation Page")
        self.geometry("800x600")
        self.configure(bg="#f4f4f4")
        self.username = username
        self.account_type = account_type

        self.events_file = "donation_events.json"
        self.donation_events = self.load_events()

        self.label_welcome = tk.Label(self, text=f"Donation Events, {self.username}", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#333")
        self.label_welcome.pack(pady=20)

        add_event_button = tk.Button(self, text="Add Donation Event", font=("Arial", 12), bg="#388e3c", fg="white", command=self.open_biodata_form)
        add_event_button.pack(pady=10)

        self.donation_frame = tk.Frame(self)
        self.donation_frame.pack(pady=10, fill=tk.X)
        self.create_donation_buttons()

        self.nav_bar = tk.Frame(self, bg="#00796b", height=50)
        self.nav_bar.pack(side=tk.BOTTOM, fill=tk.X)

        home_button = tk.Button(self.nav_bar, text="Homepage", font=("Arial", 12), bg="#004d40", fg="white", command=self.go_to_homepage)
        home_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        search_button = tk.Button(self.nav_bar, text="Search Page", font=("Arial", 12), bg="#388e3c", fg="white", command=self.go_to_searchpage)
        search_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        donation_button = tk.Button(self.nav_bar, text="Donation Page", font=("Arial", 12), bg="#d32f2f", fg="white", command=self.go_to_donasi)
        donation_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        profile_button = tk.Button(self.nav_bar, text="Profile", font=("Arial", 12), bg="#fbc02d", fg="white", command=self.go_to_profile)
        profile_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def create_donation_buttons(self):
        for widget in self.donation_frame.winfo_children():
            widget.destroy()
        for event in self.donation_events:
            button = tk.Button(self.donation_frame, text=event["name"], command=lambda e=event: self.show_event_description(e), font=("Arial", 12))
            button.pack(pady=10, fill=tk.X, padx=20)

            if self.username == event["creator"]:
                edit_button = tk.Button(self.donation_frame, text="Edit", command=lambda e=event: self.edit_event(e), font=("Arial", 10))
                edit_button.pack(pady=5)
                delete_button = tk.Button(self.donation_frame, text="Delete", command=lambda e=event: self.delete_event(e), font=("Arial", 10))
                delete_button.pack(pady=5)

    def open_biodata_form(self):
        """Open the Biodata Form before adding a new event."""
        self.withdraw()  # Hide current window
        biodata_form = Biodata_Penyelenggara(self.username)  # Open Biodata Form

        def on_biodata_complete():
            biodata_form.destroy()  # Close Biodata Form
            self.deiconify()  # Show Donation Page
            self.open_event_details_form()  # Proceed to Event Details Form

        biodata_form.protocol("WM_DELETE_WINDOW", on_biodata_complete)  # Ensure that the form closes properly

    def open_event_details_form(self):
        """Open a new form for event-specific details."""
        self.withdraw()  # Hide current window
        event_form = tk.Toplevel(self)
        event_form.title("Event Details")
        event_form.geometry("400x500")

        tk.Label(event_form, text="Nama Event:", font=("Arial", 12)).pack(pady=10)
        entry_name = tk.Entry(event_form, width=30)
        entry_name.pack()

        tk.Label(event_form, text="Deskripsi:", font=("Arial", 12)).pack(pady=10)
        entry_description = tk.Entry(event_form, width=30)
        entry_description.pack()

        tk.Label(event_form, text="Jumlah Pakaian yang Dibutuhkan:", font=("Arial", 12)).pack(pady=10)
        entry_quantity = tk.Entry(event_form, width=30)
        entry_quantity.pack()

        tk.Label(event_form, text="Jenis Pakaian yang Dibutuhkan:", font=("Arial", 12)).pack(pady=10)
        entry_type = tk.Entry(event_form, width=30)
        entry_type.pack()

        tk.Label(event_form, text="Timeline Donasi:", font=("Arial", 12)).pack(pady=10)
        entry_timeline = tk.Entry(event_form, width=30)
        entry_timeline.pack()

        def submit_event():
            event_data = {
                "name": entry_name.get(),
                "description": entry_description.get(),
                "quantity": entry_quantity.get(),
                "type": entry_type.get(),
                "timeline": entry_timeline.get(),
                "creator": self.username,
            }
            self.donation_events.append(event_data)
            self.save_events()
            messagebox.showinfo("Event Added", "Your donation event has been added successfully!")
            event_form.destroy()
            self.deiconify()  # Show Donation Page
            self.create_donation_buttons()

        tk.Button(event_form, text="Submit", command=submit_event, bg="#388e3c", fg="white", font=("Arial", 12)).pack(pady=20)

    def show_event_description(self, event):
        description_window = tk.Toplevel(self)
        description_window.title(event["name"])
        description_window.geometry("400x400")

        label_name = tk.Label(description_window, text=event["name"], font=("Arial", 16, "bold"))
        label_name.pack(pady=10)

        text_description = tk.Text(description_window, wrap=tk.WORD, font=("Arial", 12))
        text_description.insert(tk.END, event["description"])
        text_description.config(state=tk.DISABLED)
        text_description.pack(pady=10, padx=20)

        tk.Label(description_window, text="Donor Contributions:", font=("Arial", 12, "bold")).pack(pady=5)
        contributions_frame = tk.Frame(description_window)
        contributions_frame.pack(pady=5, padx=20, fill=tk.BOTH)

        for donor in event.get("donors", []):
            tk.Label(contributions_frame, text=f"{donor['donor']}: {donor['items']} items - {donor['notes']}", font=("Arial", 10)).pack(anchor="w")

        join_button = tk.Button(description_window, text="Join Donation", command=lambda: self.join_donation_event(event), font=("Arial", 12))
        join_button.pack(pady=10)

    def join_donation_event(self, event):
        join_window = tk.Toplevel(self)
        join_window.title("Join Donation")
        join_window.geometry("300x300")

        tk.Label(join_window, text="Number of Items:", font=("Arial", 12)).pack(pady=5)
        entry_items = tk.Entry(join_window, width=20)
        entry_items.pack(pady=5)

        tk.Label(join_window, text="Notes:", font=("Arial", 12)).pack(pady=5)
        entry_notes = tk.Entry(join_window, width=20)
        entry_notes.pack(pady=5)

        def submit_donation():
            items = entry_items.get()
            notes = entry_notes.get()
            if items.isdigit() and notes:
                donation = {"donor": self.username, "items": int(items), "notes": notes}
                event.setdefault("donors", []).append(donation)
                self.save_events()
                messagebox.showinfo("Thank You", "Your donation has been recorded.")
                join_window.destroy()
            else:
                messagebox.showwarning("Input Error", "Please enter valid details.")

        tk.Button(join_window, text="Submit", command=submit_donation, font=("Arial", 12), bg="#4caf50", fg="white").pack(pady=20)

    def go_to_homepage(self):
        messagebox.showinfo("Navigation", "Going to Homepage.")

    def go_to_searchpage(self):
        messagebox.showinfo("Navigation", "Going to Search Page.")

    def go_to_profile(self):
        messagebox.showinfo("Navigation", "Going to Profile.")

    def go_to_donasi(self): 
        messagebox.showinfo("Navigation", "Already in Donation Page.")

    def load_events(self):
        if os.path.exists(self.events_file):
            with open(self.events_file, "r") as f:
                return json.load(f)
        return []

    def save_events(self):
        with open(self.events_file, "w") as f:
            json.dump(self.donation_events, f, indent=4)

    def edit_event(self, event):
        event_form = tk.Toplevel(self)
        event_form.title("Edit Event")
        event_form.geometry("400x500")

        tk.Label(event_form, text="Nama Event:", font=("Arial", 12)).pack(pady=10)
        entry_name = tk.Entry(event_form, width=30)
        entry_name.insert(tk.END, event["name"])
        entry_name.pack()

        tk.Label(event_form, text="Deskripsi:", font=("Arial", 12)).pack(pady=10)
        entry_description = tk.Entry(event_form, width=30)
        entry_description.insert(tk.END, event["description"])
        entry_description.pack()

        tk.Label(event_form, text="Jumlah Pakaian yang Dibutuhkan:", font=("Arial", 12)).pack(pady=10)
        entry_quantity = tk.Entry(event_form, width=30)
        entry_quantity.insert(tk.END, event["quantity"])
        entry_quantity.pack()

        tk.Label(event_form, text="Jenis Pakaian yang Dibutuhkan:", font=("Arial", 12)).pack(pady=10)
        entry_type = tk.Entry(event_form, width=30)
        entry_type.insert(tk.END, event["type"])
        entry_type.pack()

        tk.Label(event_form, text="Timeline Donasi:", font=("Arial", 12)).pack(pady=10)
        entry_timeline = tk.Entry(event_form, width=30)
        entry_timeline.insert(tk.END, event["timeline"])
        entry_timeline.pack()

        def save_edited_event():
            event["name"] = entry_name.get()
            event["description"] = entry_description.get()
            event["quantity"] = entry_quantity.get()
            event["type"] = entry_type.get()
            event["timeline"] = entry_timeline.get()
            self.save_events()
            messagebox.showinfo("Event Edited", "The event has been updated.")
            event_form.destroy()
            self.create_donation_buttons()

        tk.Button(event_form, text="Save Changes", command=save_edited_event, bg="#388e3c", fg="white", font=("Arial", 12)).pack(pady=20)

    def delete_event(self, event):
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this event?")
        if confirm:
            self.donation_events.remove(event)
            self.save_events()
            self.create_donation_buttons()

if __name__ == "__main__":
    app = DonationPageSell(username="User1", account_type="donor")
    app.mainloop()
