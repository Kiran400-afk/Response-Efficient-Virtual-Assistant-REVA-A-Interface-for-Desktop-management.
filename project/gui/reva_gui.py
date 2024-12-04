import tkinter as tk
from tkinter import ttk, messagebox
from .styles import ModernStyle, AnimatedWidget
from .voice_activation_popup import VoiceActivationPopup

class REVA_GUI(AnimatedWidget):
    def __init__(self, master):
        self.master = master
        self.setup_window()
        self.create_widgets()
        self.voice_popup = None
        
    def setup_window(self):
        self.master.title("REVA")
        self.master.configure(bg=ModernStyle.BACKGROUND_COLOR)
        ModernStyle.apply_modern_style()
        
        # Set window size and position
        window_width = 400
        window_height = 600
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = screen_width - window_width - 20
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def create_widgets(self):
        # Main container
        self.main_frame = ttk.Frame(self.master, style="Modern.TFrame")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Header
        header_frame = ttk.Frame(self.main_frame, style="Surface.TFrame")
        header_frame.pack(fill="x", pady=(0, 20))

        self.title_label = ttk.Label(
            header_frame,
            text="REVA Assistant",
            style="Title.TLabel"
        )
        self.title_label.pack(side="left", pady=10)

        self.switch_off_button = ttk.Button(
            header_frame,
            text="Switch Off",
            command=self.switch_off,
            style="Modern.TButton"
        )
        self.switch_off_button.pack(side="right", pady=10)

        # Activity display
        self.activity_frame = ttk.Frame(self.main_frame, style="Surface.TFrame")
        self.activity_frame.pack(fill="both", expand=True)

        self.status_label = ttk.Label(
            self.activity_frame,
            text="Ready to assist",
            style="Modern.TLabel"
        )
        self.status_label.pack(pady=10)

        # Create visualization canvas
        self.canvas = tk.Canvas(
            self.activity_frame,
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

    def switch_off(self):
        self.status_label.config(text="Shutting down...")
        self.switch_off_button.config(state=tk.DISABLED)
        self.master.after(2000, self.master.destroy)

    def animate_listening(self):
        if not hasattr(self, 'voice_popup') or not self.voice_popup:
            self.voice_popup = VoiceActivationPopup(self.master)
        
        for i, bar in enumerate(self.bars):
            height = abs(50 * (i % 3))  # Create wave-like pattern
            self.canvas.coords(
                bar,
                i*36 + 10, 80 - height,
                i*36 + 30, 80
            )
        self.master.after(100, self.animate_listening)

    def stop_animation(self):
        if self.voice_popup:
            self.voice_popup.destroy()
            self.voice_popup = None
        
        for bar in self.bars:
            self.canvas.coords(
                bar,
                self.canvas.coords(bar)[0], 80,
                self.canvas.coords(bar)[2], 80
            )

    def update_status(self, text):
        self.status_label.config(text=text)