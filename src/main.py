import customtkinter as ctk
from password_checker import PasswordChecker
from gui import StyledGUI
import json
from PIL import Image, ImageTk
from database import DatabaseHandler

# Assuming PasswordGenerator is defined elsewhere and imported here
from password_generator import PasswordGenerator

class App(ctk.CTk):
    def open_generator_dialog(self):
        # Create dialog window
        self.generator_dialog = ctk.CTkToplevel(self)
        self.generator_dialog.title("Generate Password")
        self.generator_dialog.geometry("400x300")

        # Length slider
        self.length_label = ctk.CTkLabel(self.generator_dialog, text="Length: 12")
        self.length_label.pack(pady=10)
    
        self.length_slider = ctk.CTkSlider(
            self.generator_dialog,
            from_=8, to=32,
            command=lambda v: self.length_label.configure(text=f"Length: {int(v)}")
        )
        self.length_slider.set(12)
        self.length_slider.pack()

        # Character type checkboxes
        self.upper_var = ctk.BooleanVar(value=True)
        self.lower_var = ctk.BooleanVar(value=True)
        self.digit_var = ctk.BooleanVar(value=True)
        self.special_var = ctk.BooleanVar(value=True)

        ctk.CTkCheckBox(self.generator_dialog, text="Uppercase (A-Z)", variable=self.upper_var).pack(pady=5)
        ctk.CTkCheckBox(self.generator_dialog, text="Lowercase (a-z)", variable=self.lower_var).pack(pady=5)
        ctk.CTkCheckBox(self.generator_dialog, text="Digits (0-9)", variable=self.digit_var).pack(pady=5)
        ctk.CTkCheckBox(self.generator_dialog, text="Special (!@#)", variable=self.special_var).pack(pady=5)

        # Generate button
        ctk.CTkButton(
            self.generator_dialog,
            text="Generate",
            command=self.generate_and_display
        ).pack(pady=20)
        
    def generate_and_display(self):
        # Get settings from dialog
        length = int(self.length_slider.get())
        use_upper = self.upper_var.get()
        use_lower = self.lower_var.get()
        use_digits = self.digit_var.get()
        use_special = self.special_var.get()

        # Generate password
        generator = PasswordGenerator()
        try:
            password = generator.generate(length, use_upper, use_lower, use_digits, use_special)
            # Insert into main password field
            self.password_entry.delete(0, "end")
            self.password_entry.insert(0, password)
            # Close dialog
            self.generator_dialog.destroy()
        except ValueError as e:
            ctk.CTkLabel(self.generator_dialog, text="Error: Select at least one character type!", text_color="red").pack()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checker = PasswordChecker()
        self.gui = StyledGUI(self)
        self.db = DatabaseHandler()

        # Initialize breach_label
        self.breach_label = ctk.CTkLabel(self, text="Breach Status: ❌ Not Checked")
        self.breach_label.pack()

        # Window setup
        self.title("Password Checker")
        self.geometry("500x400")
        
        # Create widgets
        self.create_widgets()
        self.load_styles()

    def create_widgets(self):
         # Ensure background is loaded first
        self.gui.load_background()
        # Load images using PIL
        try:
            light_image = Image.open("../assets/icons/sun.png")
            dark_image = Image.open("../assets/icons/moon.png")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return

        # Dark mode toggle button (NEW)
        self.dark_mode_btn = ctk.CTkButton(
            self,
            text="",
            image=ctk.CTkImage(light_image=light_image, dark_image=dark_image),
            command=self.gui.toggle_dark_mode,
            width=40
        )
        self.dark_mode_btn.pack(pady=10)

        # Password Generator Button (NEW)
        self.generate_btn = ctk.CTkButton(
            self,
            text="🔑 Generate Password",
            command=self.open_generator_dialog
        )
        self.generate_btn.pack(pady=5)

        # Existing widgets below
        self.password_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter password...",
            width=300,
            height=40
        )
        self.password_entry.pack(pady=20)
        
        self.strength_bar = ctk.CTkProgressBar(self, width=300, height=20)
        self.strength_bar.pack()
        self.strength_bar.set(0)
        
        self.strength_label = ctk.CTkLabel(self, text="Strength: None")
        self.strength_label.pack(pady=10)
    
        # Password History Panel (Scrollable Frame)
        self.history_label = ctk.CTkLabel(self, text="Password Check History:", font=("Arial", 12, "bold"))
        self.history_label.pack(pady=(20, 5))  # Adds a heading for the history

        self.history_frame = ctk.CTkScrollableFrame(self, width=450, height=150)
        self.history_frame.pack(pady=(0, 10))  # Adds padding below the frame

        # Initial load of history
        self.refresh_history()
        # ------------------------------------------------

        # Real-time updates (keep this line at the end)
        self.password_entry.bind("<KeyRelease>", self.update_strength)

    def load_styles(self):
        with open("../assets/styles.json", "r") as f:
            self.styles = json.load(f)

    def update_strength(self, event=None):
        password = self.password_entry.get()
        if password:  # Only check if password is not empty
            result = self.checker.calculate_strength(password)
            if result is not None:
                strength_text, strength_value = result
                is_breached = self.checker.check_breach(password)
                # Update progress bar and label
                self.strength_bar.set(strength_value / 100)
                self.strength_label.configure(text=f"Strength: {strength_text}")
                self.breach_label.configure(
                    text=f"Breach Status: {'✅ Safe' if not is_breached else '❌ Breached!'}"
                )
                # Save to DB with breach status
                self.db.add_record(strength_value, is_breached)
                self.refresh_history()
            else:
                # Handle the case where calculate_strength returns None
                self.strength_bar.set(0)
                self.strength_label.configure(text="Strength: Error")
                self.breach_label.configure(text="Breach Status: ❌ Not Checked")
        else:
            # Reset if password field is empty
            self.strength_bar.set(0)
            self.strength_label.configure(text="Strength: None")
            self.breach_label.configure(text="Breach Status: ❌ Not Checked")

    def refresh_history(self):
        # Clear old entries in the history frame
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        # Fetch history from the database
        records = self.db.fetch_history()
        
        # Display each record
        for timestamp, score, breached in records:
            # Format the entry text
            breached_status = "✅" if breached else "❌"
            entry_text = f"{timestamp} | Score: {score}% | Breached: {breached_status}"
            
            # Create a label for each entry
            entry_label = ctk.CTkLabel(
                self.history_frame, 
                text=entry_text,
                font=("Arial", 10)
            )
            entry_label.pack(anchor="w", padx=10, pady=2)  # Align to the left

if __name__ == "__main__":
    app = App()
    app.mainloop()