import tkinter as tk
from tkinter import messagebox
from DonationPage import DonationPage  # Ensure DonationPage is correctly implemented

class MenuDaurUlang(tk.Tk):
    def __init__(self, username, account_type):
        super().__init__()
        self.username = username
        self.account_type = account_type
        self.title("MenuDaurUlang")
        self.geometry("500x600")
        self.eval('tk::PlaceWindow . center')

        self.label_title = tk.Label(self, text="BajuKita", font=("Helvetica", 20, "bold"))
        self.label_title.pack(pady=20)

        self.create_buttons()

        self.back_button = tk.Button(self, text="Back", command=self.go_back, font=("Helvetica", 12))
        self.back_button.pack(pady=10)

    def create_buttons(self):
        products = [
            ("Tas atau Tote Bag dari Kaos Lama", self.show_tutorial_tas),
            ("Sarung Bantal dari Kemeja Lama", self.show_tutorial_sarung_bantal),
            ("Scrunchie dari Potongan Kain", self.show_tutorial_scrunchie),
            ("Keset dari Kaos Bekas", self.show_tutorial_keset),
            ("Boneka dari Pakaian Bekas", self.show_tutorial_boneka),
            ("Dompet dari Celana Jeans", self.show_tutorial_dompet),
            ("Hiasan Dinding dari Potongan Kain", self.show_tutorial_hiasan_dinding),
            ("Selimut Tambal Sulam", self.show_tutorial_selimut)
        ]

        for product, command in products:
            button = tk.Button(self, text=product, command=command, font=("Helvetica", 12))
            button.pack(pady=10, fill=tk.X, padx=20)

    def show_tutorial(self, title, content):
        tutorial_window = tk.Toplevel(self)
        tutorial_window.title(title)
        tutorial_window.geometry("500x400")

        label_title = tk.Label(tutorial_window, text=title, font=("Helvetica", 16, "bold"))
        label_title.pack(pady=10)

        text_content = tk.Text(tutorial_window, wrap=tk.WORD, font=("Helvetica", 12))
        text_content.insert(tk.END, content)
        text_content.pack(pady=10, padx=20)

        back_button = tk.Button(tutorial_window, text="Back", command=tutorial_window.destroy, font=("Helvetica", 12))
        back_button.pack(pady=10)

    def show_tutorial_tas(self):
        title = "Tas atau Tote Bag dari Kaos Lama"
        content = """Yang Perlu Disiapkan:
- Kaos bekas.
- Gunting kain.
- Jarum dan benang (opsional).

Langkah-Langkah:
1. Potong bagian bawah kaos sesuai panjang tas yang diinginkan.
2. Potong lengan dan bagian leher kaos untuk membuat pegangan tas.
3. Jahit atau simpul bagian bawah kaos agar menjadi dasar tas.
4. Tas siap digunakan sebagai tas belanja atau sehari-hari."""
        self.show_tutorial(title, content)

    def show_tutorial_sarung_bantal(self):
        title = "Sarung Bantal dari Kemeja Lama"
        content = """Yang Perlu Disiapkan:
- Kemeja bekas.
- Gunting kain.
- Jarum dan benang atau mesin jahit.

Langkah-Langkah:
1. Potong kemeja membentuk persegi sesuai ukuran bantal.
2. Pastikan kancing kemeja berada di tengah untuk akses menutup sarung bantal.
3. Jahit bagian sisi kain, sisakan bagian dengan kancing terbuka.
4. Balik kain dan masukkan bantal ke dalam sarung."""
        self.show_tutorial(title, content)

    def show_tutorial_scrunchie(self):
        title = "Scrunchie dari Potongan Kain"
        content = """Yang Perlu Disiapkan:
- Potongan kain dari pakaian bekas (30 x 10 cm).
- Karet elastis (panjang 20 cm).
- Jarum dan benang atau lem kain.

Langkah-Langkah:
1. Lipat kain menjadi dua memanjang dengan sisi dalam menghadap ke luar.
2. Jahit sepanjang sisi kain, lalu balikkan kain ke sisi luar.
3. Masukkan karet elastis ke dalam kain menggunakan peniti.
4. Ikat ujung karet, lalu jahit atau lem ujung kain agar tertutup."""
        self.show_tutorial(title, content)

    def show_tutorial_keset(self):
        title = "Keset dari Kaos Bekas"
        content = """Yang Perlu Disiapkan:
- Beberapa kaos bekas.
- Gunting kain.
- Alas jaring plastik (opsional).

Langkah-Langkah:
1. Potong kaos menjadi strip panjang selebar 3-5 cm.
2. Jika menggunakan alas jaring, ikat setiap strip ke jaring hingga penuh.
3. Jika tidak menggunakan alas, rajut atau kepang strip kain menjadi bentuk keset.
4. Rapikan ujung kain dan pastikan keset kokoh."""
        self.show_tutorial(title, content)

    def show_tutorial_boneka(self):
        title = "Boneka dari Pakaian Bekas"
        content = """Yang Perlu Disiapkan: 
- Potongan kain bekas.
- Pola boneka (opsional).
- Isian (kapas atau potongan kain kecil).
- Jarum dan benang.

Langkah-Langkah:
1. Gambar pola boneka pada kain, lalu gunting.
2. Jahit dua potongan kain mengikuti pola, sisakan celah kecil.
3. Balikkan kain ke sisi luar, lalu isi dengan kapas atau kain kecil.
4. Jahit celah hingga tertutup. Tambahkan detail seperti mata atau hidung menggunakan benang."""
        self.show_tutorial(title, content)

    def show_tutorial_dompet(self):
        title = "Dompet dari Celana Jeans"
        content = """Yang Perlu Disiapkan:
- Celana jeans bekas.
- Gunting kain.
- Ritsleting.
- Jarum dan benang atau mesin jahit.

Langkah-Langkah:
1. Potong bagian saku belakang jeans untuk dijadikan dasar dompet.
2. Jahit bagian bawah dan samping saku.
3. Pasang ritsleting di bagian atas menggunakan jarum dan benang.
4. Dompet siap digunakan untuk menyimpan uang atau barang kecil."""
        self.show_tutorial(title, content)

    def show_tutorial_hiasan_dinding(self):
        title = "Hiasan Dinding dari Potongan Kain"
        content = """Yang Perlu Disiapkan:
- Potongan kain bekas.
- Lem tembak atau lem kain.
- Papan kanvas atau bingkai kayu.

Langkah-Langkah:
1. Potong kain menjadi bentuk geometris atau pola tertentu.
2. Tempel kain pada papan kanvas atau bingkai sesuai pola.
3. Biarkan kering, lalu gantung di dinding sebagai dekorasi."""
        self.show_tutorial(title, content)

    def show_tutorial_selimut(self):
        title = "Selimut Tambal Sulam"
        content = """Yang Perlu Disiapkan:
- Beberapa pakaian bekas dengan pola atau warna berbeda.
- Gunting kain.
- Mesin jahit atau jarum dan benang.

Langkah-Langkah:
1. Potong kain menjadi potongan persegi atau bentuk lain dengan ukuran seragam.
2. Susun potongan kain hingga membentuk pola atau desain yang diinginkan.
3. Jahit setiap potongan kain hingga menjadi satu lembar besar.
4. Tambahkan lapisan bawah untuk kenyamanan, lalu jahit sisi luar selimut."""
        self.show_tutorial(title, content)

    def go_back(self):
        """Closes the current window and opens the DonationPage."""
        self.destroy()  # Close this window
        DonationPage(self.username, self.account_type)  # Open the DonationPage window

if __name__ == "__main__":
    app = MenuDaurUlang("Seller1", "seller")  # Example values for username and account_type
    app.mainloop()
