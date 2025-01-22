import tkinter as tk
from tkinter import filedialog, messagebox
from AIFiturDonation import AI_Donation


class BiodataBajuThrifting(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BajuKita")
        self.geometry("500x600")
        self.eval('tk::PlaceWindow . center')

        # Title Label (persists across pages)
        self.label_title = tk.Label(self, text="Form Informasi Baju", font=("Helvetica", 14, "bold"))
        self.label_title.pack(pady=10)

        # Frame for content
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Start with the first page
        self.show_page1()

        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def show_page1(self):
        self.clear_frame()

        questions = ["Ukuran:", "Kondisi:", "Merek:", "Warna:", "Jenis Bahan:"]

        self.entries_page1 = {}
        for question in questions:
            label = tk.Label(self.main_frame, text=question, font=("Helvetica", 10))
            label.pack(pady=5)
            entry = tk.Entry(self.main_frame, width=30)
            entry.pack(pady=5)
            self.entries_page1[question] = entry

        self.create_navigation_buttons(self.show_page2)

    def show_page2(self):
        self.clear_frame()

        questions = ["Riwayat Penyakit:", "Jenis Kelamin:", "Alamat Email:", "Alasan Penyumbangan/Penjualan:"]

        self.entries_page2 = {}
        for question in questions:
            label = tk.Label(self.main_frame, text=question, font=("Helvetica", 10))
            label.pack(pady=5)
            entry = tk.Entry(self.main_frame, width=30)
            entry.pack(pady=5)
            self.entries_page2[question] = entry

        self.create_navigation_buttons(submit=True, back_command=self.show_page1)

    def create_navigation_buttons(self, next_command=None, back_command=None, submit=False):
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=20, fill="x")

        if back_command:
            button_back = tk.Button(button_frame, text="Back", command=back_command)
            button_back.pack(side=tk.LEFT, padx=20)

        if next_command:
            button_next = tk.Button(button_frame, text="Next", command=next_command)
            button_next.pack(side=tk.RIGHT, padx=20)

        elif submit:
            button_submit = tk.Button(button_frame, text="Submit", command=self.submit_organization)
            button_submit.pack(side=tk.RIGHT, padx=20)

    def submit_organization(self):
        # Collect data from both pages
        data_page1 = {question: entry.get() for question, entry in self.entries_page1.items()}
        data_page2 = {question: entry.get() for question, entry in self.entries_page2.items()}

        # Show a confirmation message
        messagebox.showinfo("Submission Successful", "Your data has been submitted!")

        # Transition to AI Scan Fitur
        self.destroy()  # Close the current form
        ai_scan_app = AI_Donation()
        ai_scan_app.mainloop()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()

    def on_exit(self):
        self.destroy()


    def upload_image(self):
        # Placeholder for upload functionality
        messagebox.showinfo("Upload", "Upload Gambar functionality is not implemented.")

    def open_camera(self):
        # Placeholder for camera functionality
        messagebox.showinfo("Camera", "Camera functionality is not implemented.")


if __name__ == "__main__":
    app = BiodataBajuThrifting()
    app.mainloop()
