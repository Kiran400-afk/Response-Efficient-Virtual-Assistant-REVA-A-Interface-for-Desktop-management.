import tkinter as tk
from tkinter import ttk
from .styles import ModernStyle

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        self.master.title("REVA Assistant")
        self.master.configure(bg=ModernStyle.BACKGROUND_COLOR)
        ModernStyle.apply_modern_style()
        
        # Set window size and position
        window_width = 400
        window_height = 600
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def create_widgets(self):
        # Main container
        self.main_frame = ttk.Frame(self.master, style="Modern.TFrame")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Header
        self.title_label = ttk.Label(
            self.main_frame,
            text="REVA Assistant",
            style="Title.TLabel"
        )
        self.title_label.pack(pady=10)

        # Status display
        self.status_label = ttk.Label(
            self.main_frame,
            text="Listening...",
            style="Modern.TLabel"
        )
        self.status_label.pack(pady=10)

        # Voice activity visualization
        self.canvas = tk.Canvas(
            self.main_frame,
            width=360,
            height=100,
            bg=ModernStyle.SURFACE_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(pady=20)
        
        # Create voice activity bars
        self.bars = []
        for i in range(10):
            bar = self.canvas.create_rectangle(
                i*36 + 10, 80,
                i*36 + 30, 80,
                fill=ModernStyle.PRIMARY_COLOR
            )
            self.bars.append(bar)

    def update_status(self, text):
        self.status_label.config(text=text)

    def animate_listening(self):
        import random
        for bar in self.bars:
            height = random.randint(10, 60)
            self.canvas.coords(
                bar,
                self.canvas.coords(bar)[0], 80 - height,
                self.canvas.coords(bar)[2], 80
            )