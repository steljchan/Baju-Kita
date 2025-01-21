import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import Homepage
import os

USER_FILE = "users.txt"
MESSAGE_FILE = "messages.txt"  # Stores chat messages

class ChatApp(tk.Tk):
    def __init__(self, username, account_type):
        super().__init__()
        self.username = username
        self.account_type = account_type
        self.chat_with = None
        self.title("Chat Menu")
        self.geometry("500x600")
        self.configure(bg="#f0f0f0")
        self.load_user_menu()

    def load_user_menu(self):
        """Display the menu of available users."""
        self.clear_widgets()
        tk.Label(self, text=f"Welcome, {self.username}!", font=("Helvetica", 16), bg="#f0f0f0", fg="#333").pack(pady=10)

        all_users = self.get_all_users()
        if self.username in all_users:
            all_users.remove(self.username)

        if not all_users:
            tk.Label(self, text="No other users are available.", font=("Helvetica", 12), bg="#f0f0f0", fg="#333").pack(pady=20)
        else:
            tk.Label(self, text="Available Users:", font=("Helvetica", 12), bg="#f0f0f0", fg="#333").pack(pady=10)
            for user in all_users:
                tk.Button(self, text=user, width=25, command=lambda u=user: self.open_chat(u), bg="#4CAF50", fg="white", font=("Helvetica", 12)).pack(pady=5)

        tk.Button(self, text="Back", command=self.go_to_homepage, bg="#FF6347", fg="white", font=("Helvetica", 12)).pack(pady=10)

    def get_all_users(self):
        users = []
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r") as file:
                users = [line.split(",")[0] for line in file if line.strip()]
        return users

    def open_chat(self, other_user):
        """Open the chat interface with another user."""
        self.clear_widgets()
        self.chat_with = other_user

        # Back button
        back_button = tk.Button(self, text="Back", command=self.load_user_menu, bg="#FF6347", fg="white", font=("Helvetica", 12))
        back_button.pack(anchor="ne", padx=10, pady=10)

        # Chat title
        tk.Label(self, text=f"Chat with {other_user}", font=("Helvetica", 16), bg="#f0f0f0", fg="#333").pack(pady=10)

        # Chat display area
        self.chat_canvas = tk.Canvas(self, bg="#f0f0f0", width=480, height=400, highlightthickness=0)
        self.chat_canvas.pack(pady=10)

        self.scroll_y = tk.Scrollbar(self, orient="vertical", command=self.chat_canvas.yview)
        self.scroll_y.pack(side="right", fill="y")
        self.chat_canvas.configure(yscrollcommand=self.scroll_y.set)

        self.chat_frame = tk.Frame(self.chat_canvas, bg="#f0f0f0")
        self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        self.chat_frame.bind("<Configure>", lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))

        # Load chat history
        self.load_chat_history()

        # Message entry and buttons
        message_frame = tk.Frame(self, bg="#f0f0f0")
        message_frame.pack(fill="x", pady=10)

        self.entry_message = tk.Entry(message_frame, width=35, font=("Helvetica", 12))
        self.entry_message.pack(side="left", padx=5)

        send_button = tk.Button(message_frame, text="Send", command=self.send_message, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        send_button.pack(side="left", padx=5)

        upload_button = tk.Button(message_frame, text="Upload Image", command=self.upload_image, bg="#2196F3", fg="white", font=("Helvetica", 12))
        upload_button.pack(side="left", padx=5)


    def load_chat_history(self):
        """Load and display the chat history with another user."""
        for widget in self.chat_frame.winfo_children():
            widget.destroy()

        if os.path.exists(MESSAGE_FILE):
            with open(MESSAGE_FILE, "r") as file:
                for line in file:
                    try:
                        sender, recipient, content = line.strip().split(",", 2)
                        if (sender == self.username and recipient == self.chat_with) or \
                                (sender == self.chat_with and recipient == self.username):
                            if content.startswith("Image: "):
                                self.add_bubble(sender, image=content.replace("Image: ", "").strip())
                            else:
                                self.add_bubble(sender, text=content.strip())
                    except ValueError:
                        continue

    def add_bubble(self, sender, text=None, image=None):
        """Add a chat bubble to the chat frame."""
        frame = tk.Frame(self.chat_frame, bg="#f0f0f0")
        
        if sender == self.username:
            # User's messages go to the right
            frame.pack(anchor="e", pady=5)
            bg_color = "#DCF8C6"  # Greenish color for user's bubble
        else:
            # Other user's messages go to the left
            frame.pack(anchor="w", pady=5)
            bg_color = "#ADD8E6"  # Blueish color for other user's bubble


        # Add text message
        if text:
            tk.Label(frame, text=text, wraplength=250, bg=bg_color, fg="#333", font=("Helvetica", 12), padx=10, pady=5).pack()

        # Add image if it's an image message
        elif image:
            if os.path.exists(image):
                img = Image.open(image)
                img.thumbnail((150, 150))
                img = ImageTk.PhotoImage(img)
                img_label = tk.Label(frame, image=img, bg=bg_color)
                img_label.image = img  # Keep a reference to the image
                img_label.pack()


    def send_message(self):
        """Send a text message to another user."""
        if not self.chat_with:
            return

        message = self.entry_message.get().strip()
        if message:
            with open(MESSAGE_FILE, "a") as file:
                file.write(f"{self.username},{self.chat_with},{message}\n")
            self.entry_message.delete(0, tk.END)
            self.load_chat_history()


    def upload_image(self):
        """Upload and send an image."""
        if not self.chat_with:
            return

        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if filepath:
            with open(MESSAGE_FILE, "a") as file:
                file.write(f"{self.username},{self.chat_with},Image: {filepath}\n")
            self.load_chat_history()

    def clear_widgets(self):
        """Clear all widgets in the window."""
        for widget in self.winfo_children():
            widget.destroy()

    def go_to_homepage(self):
        self.destroy()
        app = Homepage.Homepage(username=self.username, account_type=self.account_type)
        app.mainloop()

if __name__ == "__main__":
    username = "User_A"
    account_type = "customer"
    app = ChatApp(username, account_type)
    app.mainloop()
