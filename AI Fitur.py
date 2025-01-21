import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import cv2
import random

class BajuKitaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BajuKita - AI Scan")
        self.geometry("500x600")
        self.eval('tk::PlaceWindow . center')

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
            response = messagebox.showinfo("Upload Status", "Pakaian kamu berhasil terupload")
            if response == 'ok':
                self.on_exit()
        else:
            response = messagebox.showerror("Upload Status", "Maaf, pakaian kamu tidak bisa diupload. Mungkin kamu bisa mendaur ulang baju kamu!")
            if response == 'ok':
                self.show_recycle_page()

    def open_camera(self):
        self.button_upload.pack_forget()  # Hide the upload button
        self.button_camera.pack_forget()  # Hide the take picture button
        self.cap = cv2.VideoCapture(0)
        frame_width = 210  # Example: Set width to 640 pixels
        frame_height = 120  # Example: Set height to 480 pixels
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
        self.show_camera = True
        self.show_frame()
        self.button_capture.pack(side="bottom", pady=10)  # Show the capture button when the camera is open

    def show_frame(self):
        if self.show_camera:
            ret, frame = self.cap.read()
            if ret:
                self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame = Image.fromarray(self.frame)
                self.frame = ImageTk.PhotoImage(self.frame)
                self.image_label.config(image=self.frame)
                self.image_label.image = self.frame
                self.button_capture.lift()  # Ensure the capture button is at the top
            self.after(10, self.show_frame)

    def capture_image(self):
        if self.show_camera:
            # Stop the camera display
            self.show_camera = False
            
            # Capture the frame
            ret, self.frame = self.cap.read()
            if not ret or self.frame is None:
                raise ValueError("Failed to capture frame from the camera.")
            
            # Process and save the captured image
            try:
                image = Image.fromarray(cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))
                image = image.resize((300, 300), Image.Resampling.NEAREST)
                image.save("captured_image.jpg")  # Save the captured image

                # Update the UI with the captured image
                image_tk = ImageTk.PhotoImage(image)
                self.image_label.config(image=image_tk)
                self.image_label.image = image_tk

                # Hide the capture button
                self.button_capture.pack_forget()

                # Start the scan of the captured image
                self.simulate_scan(image)

            except cv2.error as e:
                raise RuntimeError(f"OpenCV error during image processing: {e}")

            finally:
                # Release the camera
                self.cap.release()


    def check_clothes_condition(self, image):
        # Simulate the condition check
        return random.choice([True, False])

    def show_recycle_page(self):
        recycle_page = tk.Toplevel(self)
        recycle_page.title("Recycle Page")
        recycle_page.geometry("500x600")
        tk.Label(recycle_page, text="Silakan daur ulang baju kamu!").pack(pady=20)
        tk.Button(recycle_page, text="Tutup", command=recycle_page.destroy).pack(pady=10)

    def on_exit(self):
        if self.cap:
            self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = BajuKitaApp()
    app.mainloop()
