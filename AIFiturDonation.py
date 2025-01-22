import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import cv2
import random
from PilihDaurUlang import MenuDaurUlang    

class AI_Donation(tk.Tk):
    def __init__(self, username=None, account_type=None):
        super().__init__()
        self.title("BajuKita - AI Scan")
        self.geometry("500x600")
        self.eval('tk::PlaceWindow . center')

        # Store user information
        self.username = username
        self.account_type = account_type

        self.label_title = tk.Label(self, text="Upload atau Foto Baju Kamu", font=("Helvetica", 14, "bold"))
        self.label_title.pack(pady=20)

        self.button_upload = tk.Button(self, text="Upload Gambar", command=self.upload_image)
        self.button_upload.pack(pady=10)

        self.button_camera = tk.Button(self, text="Buka Kamera", command=self.open_camera)
        self.button_camera.pack(pady=10)

        self.button_capture = tk.Button(self, text="Ambil Gambar", command=self.capture_image)
        self.button_capture.pack_forget()  # Hide the button initially

        self.image_label = tk.Label(self)
        self.image_label.pack(pady=20)

        self.result_label = tk.Label(self, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=20)

        self.cap = None
        self.frame = None
        self.show_camera = False

        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def upload_image(self):
        filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if filename:
            image = Image.open(filename)
            image = image.resize((300, 300), Image.Resampling.NEAREST)
            image_tk = ImageTk.PhotoImage(image)

            self.image_label.config(image=image_tk)
            self.image_label.image = image_tk

            self.button_upload.pack_forget()  # Hide the upload button
            self.button_camera.pack_forget()  # Hide the take picture button

            self.simulate_scan(image)

    def simulate_scan(self, image):
        for y in range(0, 300, 10):
            image_with_line = image.copy()
            draw = ImageDraw.Draw(image_with_line)
            draw.line((0, y, 300, y), fill="green", width=3)

            image_tk = ImageTk.PhotoImage(image_with_line)
            self.image_label.config(image=image_tk)
            self.image_label.image = image_tk
            self.update()
            self.after(50)

        # Simulate the AI condition check
        if self.check_clothes_condition(image):
            messagebox.showinfo("Upload Status", "Pakaian kamu berhasil terupload")
            self.on_exit()
        else:
            messagebox.showerror("Upload Status", "Maaf, pakaian kamu tidak bisa diupload. Mungkin kamu bisa mendaur ulang baju kamu!")
            self.show_recycle_page()

    def open_camera(self):
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.show_camera = True
        self.show_frame()
        self.button_capture.pack(side="bottom", pady=10)  # Show the capture button

    def show_frame(self):
        if self.show_camera:
            ret, frame = self.cap.read()
            if ret:
                self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame = Image.fromarray(self.frame)
                self.frame = self.frame.resize((300, 300), Image.Resampling.NEAREST)
                self.frame = ImageTk.PhotoImage(self.frame)
                self.image_label.config(image=self.frame)
                self.image_label.image = self.frame
            self.after(10, self.show_frame)

    def capture_image(self):
        if self.show_camera:
            self.show_camera = False
            ret, frame = self.cap.read()
            if ret:
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                image = image.resize((300, 300), Image.Resampling.NEAREST)
                image.save("captured_image.jpg")  # Save the captured image

                image_tk = ImageTk.PhotoImage(image)
                self.image_label.config(image=image_tk)
                self.image_label.image = image_tk

                self.button_capture.pack_forget()  # Hide the capture button
                self.simulate_scan(image)

            self.cap.release()  # Release the camera

    def check_clothes_condition(self, image):
        # Simulate the condition check
        return random.choice([True, False])

    def show_recycle_page(self):
        """Launch the MenuDaurUlang app."""
        self.destroy()  # Close the current application window
        recycle_app = MenuDaurUlang(self.username, self.account_type)
        recycle_app.mainloop()

    def on_exit(self):
        """Handle cleanup and navigate back to DonationPage."""
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        self.destroy()  # Close the current window
        from DonationPage import DonationPage
        app = DonationPage(username=self.username, account_type=self.account_type)
        app.mainloop()


if __name__ == "__main__":
    app = AI_Donation(username="User123", account_type="Regular")
    app.mainloop()
