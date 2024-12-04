import tkinter as tk
from tkinter import ttk
import random

class GUIManager:
    def __init__(self, master):
        self.master = master
        master.title("REVA Assistant")
        master.configure(bg='#1E1E1E')
        
        self.setup_styles()
        self.setup_gui()

    def setup_styles(self):
        style = ttk.Style()
        style.configure('Main.TFrame', background='#1E1E1E')
        style.configure('Header.TLabel', 
                       background='#1E1E1E',
                       foreground='#FFFFFF',
                       font=('Helvetica', 24, 'bold'))
        style.configure('Status.TLabel',
                       background='#2D2D2D',
                       foreground='#00CF6B',
                       font=('Helvetica', 12))
        style.configure('Control.TButton',
                       background='#2D7FF9',
                       foreground='#FFFFFF',
                       padding=10)

    def setup_gui(self):
        self.main_frame = ttk.Frame(self.master, style='Main.TFrame')
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.create_header()
        self.create_status_display()
        self.create_visualization()
        self.create_controls()

    def create_header(self):
        self.header_label = ttk.Label(
            self.main_frame,
            text="REVA Assistant",
            style='Header.TLabel'
        )
        self.header_label.pack(pady=(0, 20))

    def create_status_display(self):
        self.status_label = ttk.Label(
            self.main_frame,
            text="Ready to assist...",
            style='Status.TLabel'
        )
        self.status_label.pack(pady=10)

    def create_visualization(self):
        self.canvas = tk.Canvas(
            self.main_frame,
            width=400,
            height=100,
            bg='#2D2D2D',
            highlightthickness=0
        )
        self.canvas.pack(pady=20)
        
        self.bars = []
        for i in range(10):
            bar = self.canvas.create_rectangle(
                i*40 + 10, 80,
                i*40 + 30, 80,
                fill='#2D7FF9'
            )
            self.bars.append(bar)

    def create_controls(self):
        self.control_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        self.control_frame.pack(pady=20)
        
        self.voice_button = ttk.Button(
            self.control_frame,
            text="🎤 Start Listening",
            style='Control.TButton',
            command=self.toggle_listening
        )
        self.voice_button.pack()

    def toggle_listening(self):
        if self.voice_button['text'] == "🎤 Start Listening":
            self.voice_button['text'] = "⏹ Stop Listening"
            self.status_label['text'] = "Listening..."
            self.animate_bars()
        else:
            self.voice_button['text'] = "🎤 Start Listening"
            self.status_label['text'] = "Ready to assist..."
            self.stop_animation()

    def animate_bars(self):
        if self.voice_button['text'] == "⏹ Stop Listening":
            for bar in self.bars:
                height = random.randint(10, 60)
                self.canvas.coords(
                    bar,
                    self.canvas.coords(bar)[0],
                    80 - height,
                    self.canvas.coords(bar)[2],
                    80
                )
            self.master.after(100, self.animate_bars)

    def stop_animation(self):
        for bar in self.bars:
            self.canvas.coords(
                bar,
                self.canvas.coords(bar)[0],
                80,
                self.canvas.coords(bar)[2],
                80
            )

    def update_status(self, text):
        self.status_label['text'] = text
