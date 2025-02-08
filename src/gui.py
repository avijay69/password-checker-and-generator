import os
from PIL import Image, ImageTk
import customtkinter as ctk
import json
import tkinter as tk

class StyledGUI:
    def __init__(self, root):
        self.root = root
        self.dark_mode = False
        self.load_styles()
        self.load_background()
        
        # Throttle window resize events
        self.resize_delay = 100  # milliseconds
        self.resize_job = None

        # Bind the resize event
        self.root.bind("<Configure>", self.on_resize)

    def load_background(self):
        # Get absolute path to background image
        current_dir = os.path.dirname(__file__)
        project_root = os.path.dirname(current_dir)
        background_path = os.path.join(
            project_root, "assets", "backgrounds", "background.jpg"
        )
        self.background_path = background_path
        self.update_background_image()

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        theme = "dark" if self.dark_mode else "light"
        ctk.set_appearance_mode(theme)
        self.update_colors(theme)
        self.update_background_image()

    def update_colors(self, theme):
        colors = self.styles[theme]
        self.root.configure(fg_color=colors["bg"])

    def update_background_image(self):
        # Load the image
        image = Image.open(self.background_path)

        # Resize the image to fit the window
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        resized_image = image.resize((window_width, window_height), Image.LANCZOS)

        # Convert the image to a format that Tkinter can use
        self.background_image = ImageTk.PhotoImage(resized_image)

        # Create a label to display the image
        if hasattr(self, 'background_label'):
            self.background_label.configure(image=self.background_image)
        else:
            self.background_label = tk.Label(self.root, image=self.background_image)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.background_label.lower()  # Send the background label to the back

    def on_resize(self, event):
        if self.resize_job is not None:
            self.root.after_cancel(self.resize_job)
        self.resize_job = self.root.after(self.resize_delay, self.update_background_image)

    def load_styles(self):
        current_dir = os.path.dirname(__file__)
        project_root = os.path.dirname(current_dir)
        styles_path = os.path.join(project_root, "assets", "styles.json")
        with open(styles_path, "r") as f:
            self.styles = json.load(f)