import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import Homepage
import SearchBar
import Profile

class DonationPage(tk.Tk):
    def __init__(self, username, account_type):
        super().__init__()
        self.title("Donation Page")
        self.geometry("800x600")
        self.configure(bg="#f4f4f4")
        self.username = username
        self.account_type = account_type

        self.events_file = "donation_events.json"
        self.donation_events = self.load_events()

        self.label_welcome = tk.Label(
            self, text=f"Welcome, {self.username}", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#333"
        )
        self.label_welcome.pack(pady=20)

        if self.account_type == "seller":
            add_event_button = tk.Button(
                self, text="Add Donation Event", font=("Arial", 12), bg="#388e3c", fg="white", command=self.open_biodata_form
            )
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
        if self.account_type == "seller":
            events = [event for event in self.donation_events if event["creator"] == self.username]
        else:  # customer
            events = self.donation_events

        for event in events:
            button = tk.Button(
                self.donation_frame,
                text=event["name"],
                command=lambda e=event: self.show_event_description(e),
                font=("Arial", 12),
            )
            button.pack(pady=10, fill=tk.X, padx=20)

    def open_biodata_form(self):
        """Open the Biodata Form before adding a new event."""
        self.withdraw()  # Hide current window
        from BiodataPenyelenggaraDonasi import Biodata_Penyelenggara
        biodata_form = Biodata_Penyelenggara(callback=self.on_biodata_complete)  # Pass the callback

    def on_biodata_complete(self):
        """Called when the biodata form is complete."""
        self.deiconify()  # Show Donation Page
        self.open_event_details_form()  # Proceed to Event Details Form

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

        # Event Name
        label_name = tk.Label(description_window, text=event["name"], font=("Arial", 16, "bold"))
        label_name.pack(pady=10)

        # Event Details
        details_frame = tk.Frame(description_window)
        details_frame.pack(pady=10, padx=20, fill=tk.BOTH)

        tk.Label(details_frame, text="Description:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(details_frame, text=event["description"], font=("Arial", 12)).grid(row=0, column=1, sticky="w", padx=10)

        tk.Label(details_frame, text="Timeline:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w")
        tk.Label(details_frame, text=event["timeline"], font=("Arial", 12)).grid(row=1, column=1, sticky="w", padx=10)

        tk.Label(details_frame, text="Type:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w")
        tk.Label(details_frame, text=event["type"], font=("Arial", 12)).grid(row=2, column=1, sticky="w", padx=10)

        tk.Label(details_frame, text="Quantity:", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="w")
        tk.Label(details_frame, text=event["quantity"], font=("Arial", 12)).grid(row=3, column=1, sticky="w", padx=10)

        # Donor Contributions Section
        tk.Label(description_window, text="Donor Contributions:", font=("Arial", 12, "bold")).pack(pady=5)
        contributions_frame = tk.Frame(description_window)
        contributions_frame.pack(pady=5, padx=20, fill=tk.BOTH)

        for donor in event.get("donors", []):
            tk.Label(contributions_frame, text=f"{donor['donor']}: {donor['items']} items - {donor['notes']}", font=("Arial", 10)).pack(anchor="w")

        # Buttons Frame
        button_frame = tk.Frame(description_window)
        button_frame.pack(pady=10)

        # Back Button
        tk.Button(button_frame, text="Kembali", command=lambda: self.go_back(description_window)).pack(side=tk.LEFT, padx=10)

        # Edit Donation Button (Visible only to the creator of the event)
        if self.account_type == "seller" and event.get("creator") == self.username:
            tk.Button(
                button_frame,
                text="Edit Donation Event",
                command=lambda: [self.edit_event(event), description_window.destroy()],
                bg="#f57c00",
                fg="white",
                font=("Arial", 12),
            ).pack(side=tk.LEFT, padx=10)

        # Join Donation Button
        tk.Button(button_frame, text="Ikut Donation", command=lambda: self.join_donation_event(event)).pack(side=tk.RIGHT, padx=10)

    def go_back(self, window):
        """Close the current window and return to the donation page."""
        window.destroy()

    def open_donation_form(self):
        """Open the donation form window."""
        self.destroy()  # Close the current window
        from BiodataBajuDonasi import BiodataBajuDonasi
        donation_form = BiodataBajuDonasi()
        donation_form.mainloop()

    def launch_ai_scan_app(self):
        from AIFiturDonation import AI_Donation
        app = AI_Donation()
        app.mainloop()

    def join_donation_event(self, event):
        join_window = tk.Toplevel(self)
        join_window.title("Join Donation")
        join_window.geometry("300x300")

        tk.Label(join_window, text="Jumlah Baju:", font=("Arial", 12)).pack(pady=5)
        entry_items = tk.Entry(join_window, width=20)
        entry_items.pack(pady=5)

        tk.Label(join_window, text="Catatan:", font=("Arial", 12)).pack(pady=5)
        entry_notes = tk.Entry(join_window, width=20)
        entry_notes.pack(pady=5)

        def submit_donation():
            self.open_donation_form()
            self.launch_ai_scan_app()
            items = entry_items.get()
            notes = entry_notes.get()
            if items.isdigit() and notes:
                donation = {"donor": self.username, "items": int(items), "notes": notes}
                event.setdefault("donors", []).append(donation)
                self.save_events()
                messagebox.showinfo("Terima Kasih", "Donasi Anda Sudah Tercatat.")
                join_window.destroy()
            else:
                messagebox.showwarning("Input Salah", "Tolong isi informasi yang betul.")
        tk.Button(join_window, text="Submit", command=submit_donation, font=("Arial", 12), bg="#4caf50", fg="white").pack(pady=20)

    def go_to_homepage(self):
        self.destroy()  # Close the current Homepage
        app = Homepage.Homepage(username=self.username, account_type=self.account_type)  # Pass relevant info
        app.mainloop()

    def go_to_searchpage(self):
        self.destroy()  # Close the current Homepage
        app = SearchBar.SearchPage(username=self.username, account_type=self.account_type)  # Pass relevant info
        app.mainloop()

    def go_to_profile(self):
        self.destroy()  # Close the current Homepage
        app = Profile.profile(username=self.username, account_type=self.account_type)  # Pass relevant info
        app.mainloop()

    def go_to_donasi(self): 
        messagebox.showinfo("Navigasi", "Anda Sudah di Halaman Donasi.")

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
    
    def load_events(self):
        if os.path.exists(self.events_file):
            with open(self.events_file, "r") as f:
                return json.load(f)
        return []

    def save_events(self):
        with open(self.events_file, "w") as f:
            json.dump(self.donation_events, f, indent=4)

if __name__ == "__main__":
    app = DonationPage(username="Seller1", account_type="seller")
    app.mainloop()


