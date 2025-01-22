import tkinter as tk
from tkinter import filedialog, messagebox

class Biodata_Penyelenggara(tk.Tk):
    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self.title("Biodata Penyelenggara")
        self.geometry("500x600")
        self.eval('tk::PlaceWindow . center')

        # Title Label (persists across pages)
        self.label_title = tk.Label(self, text="Form Penyelenggara Donasi", font=("Helvetica", 14, "bold"))
        self.label_title.pack(pady=10)

        # Frame for content
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Start with the first page
        self.show_organization_page1()

        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def show_organization_page1(self):
        self.clear_frame()

        questions = ["Nama Lengkap Organisasi:", "Alamat Lengkap Kantor:",
                     "Nomor Telepon/Faksimile:", "Alamat E-mail:", "Website (jika ada):",
                     "Nomor Registrasi:"]

            
        self.entries_organization_page1 = {}
        for question in questions:
            label = tk.Label(self.main_frame, text=question, font=("Helvetica", 10))
            label.pack(pady=5)
            entry = tk.Entry(self.main_frame, width=30)
            entry.pack(pady=5)
            self.entries_organization_page1[question] = entry

        self.create_navigation_buttons(self.show_organization_page2)

    def show_organization_page2(self):
        self.clear_frame()

        questions = [
            "Visi dan Misi:", "Deskripsi Singkat Organisasi:", "Nama Ketua/Direktur:",
            "Nama Bendahara:", "Struktur Organisasi:", "Jumlah Anggota:"
        ]

        self.entries_organization_page2 = {}
        for question in questions:
            label = tk.Label(self.main_frame, text=question, font=("Helvetica", 10))
            label.pack(pady=5)
            entry = tk.Entry(self.main_frame, width=30)
            entry.pack(pady=5)
            self.entries_organization_page2[question] = entry

        self.create_navigation_buttons(self.show_organization_page3, self.show_organization_page1)

    def show_organization_page3(self):
        self.clear_frame()

        questions = [
            "Sasaran Penerima Manfaat:", "Tujuan Donasi:", "Jangka Waktu:",
            "Jenis pakaian yang dibutuhkan:", "Jumlah Pakaian yang Dibutuhkan:",
            "Kondisi Pakaian:", "Cara Pendistribusian:", "Kemitraan:"
        ]

        self.entries_organization_page3 = {}
        for question in questions:
            label = tk.Label(self.main_frame, text=question, font=("Helvetica", 10))
            label.pack(pady=5)
            entry = tk.Entry(self.main_frame, width=30)
            entry.pack(pady=5)
            self.entries_organization_page3[question] = entry

        self.create_navigation_buttons(self.show_organization_page4, self.show_organization_page2)

    def show_organization_page4(self):
        self.clear_frame()

        questions = [
            "Upload Proposal Kegiatan:", "Upload Laporan Keuangan Kegiatan:", "Upload Cara/Metode Donasi:",
            "Upload Surat keterangan resmi dari lembaga:", "Upload Laporan kegiatan sebelumnya (jika ada):",
            "Upload Sertifikat dan Penghargaan:", "Upload Dokumen Pendukung:"
        ]

        self.entries_organization_page4 = {}
        for question in questions:
            label = tk.Label(self.main_frame, text=question, font=("Helvetica", 10))
            label.pack(pady=5)
            button = tk.Button(self.main_frame, text="Upload File", command=lambda q=question: self.upload_file(q))
            button.pack(pady=5)
            self.entries_organization_page4[question] = button

        self.create_navigation_buttons(None, self.show_organization_page3, submit=True)

    def create_navigation_buttons(self, next_command=None, back_command=None, submit=False):
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=20, fill="x")

        if back_command:
            button_back = tk.Button(button_frame, text="Back", command=back_command)
            button_back.pack(side=tk.LEFT, padx=20)

        if next_command:
            button_next = tk.Button(button_frame, text="Next", command=next_command)
            button_next.pack(side=tk.RIGHT, padx=20)

        if submit:
            button_submit = tk.Button(button_frame, text="Submit", command=self.submit_organization)
            button_submit.pack(side=tk.RIGHT, padx=20)

    def upload_file(self, question):
        filename = filedialog.askopenfilename()
        if filename:
            self.entries_organization_page4[question].config(text=filename)

    def submit_organization(self):
        data_page1 = {question: entry.get() for question, entry in self.entries_organization_page1.items()}
        data_page2 = {question: entry.get() for question, entry in self.entries_organization_page2.items()}
        data_page3 = {question: entry.get() for question, entry in self.entries_organization_page3.items()}
        data_page4 = {question: entry.cget("text") for question, entry in self.entries_organization_page4.items()}

        # Show a confirmation message
        messagebox.showinfo("Submission Successful", "Your data has been submitted!")

        # Trigger the callback if it exists
        if self.callback:
            self.callback()

        self.on_exit()  # Close the application


    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()

    def on_exit(self):
        self.destroy()

if __name__ == "__main__":
    app = Biodata_Penyelenggara()
    app.mainloop()
