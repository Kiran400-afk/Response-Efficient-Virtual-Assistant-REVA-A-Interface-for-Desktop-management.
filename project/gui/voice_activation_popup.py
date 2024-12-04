import tkinter as tk
from tkinter import ttk
from .styles import ModernStyle, AnimatedWidget
import threading

class VoiceActivationPopup(tk.Toplevel, AnimatedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_window()
        self.create_widgets()
        self.fade_in(self)

    def setup_window(self):
        self.overrideredirect(True)
        self.configure(bg=ModernStyle.SURFACE_COLOR)
        self.attributes('-topmost', True)
        
        # Center the popup
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 300
        window_height = 150
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Add rounded corners and shadow effect
        self.round_corners()

    def round_corners(self):
        self.update_idletasks()
        radius = 20
        width = self.winfo_width()
        height = self.winfo_height()

        # Create rounded mask
        mask = tk.PhotoImage(width=width, height=height)
        mask.blank()
        mask.draw_arc((0, 0, radius*2, radius*2), 0, 90, fill="black")
        mask.draw_arc((0, height-radius*2, radius*2, height), 90, 180, fill="black")
        mask.draw_arc((width-radius*2, height-radius*2, width, height), 180, 270, fill="black")
        mask.draw_arc((width-radius*2, 0, width, radius*2), 270, 360, fill="black")
        mask.draw_rectangle((radius, 0, width-radius, height), fill="black")
        mask.draw_rectangle((0, radius, width, height-radius), fill="black")
        
        self._mask = mask  # Keep reference
        self.attributes('-transparentcolor', 'white')
        self.configure(bg='white')

    def create_widgets(self):
        main_frame = ttk.Frame(self, style="Surface.TFrame")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Listening indicator
        self.indicator_canvas = tk.Canvas(
            main_frame, 
            width=50, 
            height=50, 
            bg=ModernStyle.SURFACE_COLOR,
            highlightthickness=0
        )
        self.indicator_canvas.pack(pady=(0, 10))
        self.draw_listening_indicator()

        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Listening...",
            style="Title.TLabel"
        )
        self.status_label.pack(pady=5)

        # Command label
        self.command_label = ttk.Label(
            main_frame,
            text="Say 'Hey REVA' to activate",
            style="Modern.TLabel"
        )
        self.command_label.pack(pady=5)

    def draw_listening_indicator(self):
        # Create pulsing circle animation
        self.pulse_size = 20
        self.pulse_growing = True
        self.animate_pulse()

    def animate_pulse(self):
        if not self.winfo_exists():
            return

        self.indicator_canvas.delete("pulse")
        x, y = 25, 25  # Center of canvas
        
        # Draw outer pulse circle
        self.indicator_canvas.create_oval(
            x - self.pulse_size, y - self.pulse_size,
            x + self.pulse_size, y + self.pulse_size,
            fill=ModernStyle.PRIMARY_COLOR,
            tags="pulse"
        )
        
        # Draw inner solid circle
        self.indicator_canvas.create_oval(
            x - 10, y - 10, x + 10, y + 10,
            fill=ModernStyle.ACCENT_COLOR,
            tags="pulse"
        )

        # Update pulse size
        if self.pulse_growing:
            self.pulse_size += 0.5
            if self.pulse_size >= 25:
                self.pulse_growing = False
        else:
            self.pulse_size -= 0.5
            if self.pulse_size <= 20:
                self.pulse_growing = True

        self.after(50, self.animate_pulse)

    def update_status(self, text):
        self.status_label.config(text=text)

    def show_recognition(self, text):
        self.command_label.config(text=text)