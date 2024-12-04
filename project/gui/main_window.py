```python
import tkinter as tk
from tkinter import ttk
from .chat_window import ChatWindow
from .styles import Colors

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.setup_window()
        self.chat_window = ChatWindow(self.master)
        self.chat_window.pack(fill="both", expand=True)
        
    def setup_window(self):
        # Configure main window
        self.master.title("REVA Assistant")
        self.master.configure(bg=Colors.BACKGROUND)
        
        # Set window size and position
        window_width = 800
        window_height = 600
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Make window resizable
        self.master.minsize(600, 400)
        
    def update_status(self, text):
        self.chat_window.update_status(text)
        
    def add_message(self, text, is_user=False):
        self.chat_window.add_message(text, is_user)
```