```python
import tkinter as tk
from tkinter import ttk
from .styles import Colors, ModernStyle
import threading

class ChatWindow(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, style="Main.TFrame")
        ModernStyle.configure_styles()
        self.setup_gui()
        
    def setup_gui(self):
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create header
        self.create_header()
        
        # Create chat area
        self.create_chat_area()
        
        # Create status bar
        self.create_status_bar()
        
        # Create voice activation button
        self.create_voice_button()
        
    def create_header(self):
        header = ttk.Frame(self, style="Main.TFrame")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        title = ttk.Label(
            header,
            text="REVA Assistant",
            font=("Helvetica", 24, "bold"),
            foreground=Colors.TEXT,
            background=Colors.BACKGROUND
        )
        title.pack(side="left")
        
    def create_chat_area(self):
        # Create chat frame with canvas for scrolling
        self.chat_frame = ttk.Frame(self, style="Chat.TFrame")
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=20)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(
            self.chat_frame,
            background=Colors.SURFACE,
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            self.chat_frame,
            orient="vertical",
            command=self.canvas.yview
        )
        
        # Create message container
        self.message_frame = ttk.Frame(
            self.canvas,
            style="Chat.TFrame"
        )
        
        # Configure scrolling
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas_frame = self.canvas.create_window(
            (0, 0),
            window=self.message_frame,
            anchor="nw",
            width=self.canvas.winfo_reqwidth()
        )
        
        # Pack elements
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Bind events
        self.message_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
    def create_status_bar(self):
        self.status_bar = ttk.Label(
            self,
            text="Listening...",
            style="Status.TLabel"
        )
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        
    def create_voice_button(self):
        self.voice_button = ttk.Button(
            self,
            text="🎤 Voice Command",
            style="Modern.TButton",
            command=self.toggle_voice
        )
        self.voice_button.grid(row=3, column=0, pady=20)
        
    def add_message(self, text, is_user=False):
        message = ttk.Label(
            self.message_frame,
            text=text,
            wraplength=500,
            justify="left",
            style="UserMessage.TLabel" if is_user else "AssistantMessage.TLabel"
        )
        message.pack(pady=10, padx=20, anchor="e" if is_user else "w")
        
        # Scroll to bottom
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)
        
    def update_status(self, text):
        self.status_bar.config(text=text)
        
    def toggle_voice(self):
        # Toggle voice activation state
        if self.voice_button.cget("text") == "🎤 Voice Command":
            self.voice_button.config(text="⏹ Stop Listening")
            self.update_status("Listening for commands...")
        else:
            self.voice_button.config(text="🎤 Voice Command")
            self.update_status("Voice recognition stopped")
            
    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)
```