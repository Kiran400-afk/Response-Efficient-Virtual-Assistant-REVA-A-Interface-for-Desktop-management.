```python
from tkinter import ttk
import tkinter as tk

class Colors:
    PRIMARY = "#2D7FF9"
    SECONDARY = "#5856D6" 
    BACKGROUND = "#1E1E1E"
    SURFACE = "#2D2D2D"
    TEXT = "#FFFFFF"
    TEXT_SECONDARY = "#A0A0A0"
    ACCENT = "#00CF6B"
    ERROR = "#FF453A"

class ModernStyle:
    @staticmethod
    def configure_styles():
        style = ttk.Style()
        
        # Configure main window style
        style.configure(
            "Main.TFrame",
            background=Colors.BACKGROUND
        )
        
        # Configure chat frame style
        style.configure(
            "Chat.TFrame",
            background=Colors.SURFACE,
            relief="flat",
            borderwidth=0
        )
        
        # Configure message styles
        style.configure(
            "UserMessage.TLabel",
            background=Colors.PRIMARY,
            foreground=Colors.TEXT,
            padding=(20, 10),
            font=("Helvetica", 12)
        )
        
        style.configure(
            "AssistantMessage.TLabel",
            background=Colors.SURFACE,
            foreground=Colors.TEXT,
            padding=(20, 10),
            font=("Helvetica", 12)
        )
        
        # Configure status bar style
        style.configure(
            "Status.TLabel",
            background=Colors.BACKGROUND,
            foreground=Colors.TEXT_SECONDARY,
            padding=(10, 5),
            font=("Helvetica", 10)
        )
        
        # Configure buttons
        style.configure(
            "Modern.TButton",
            background=Colors.PRIMARY,
            foreground=Colors.TEXT,
            padding=(15, 8),
            font=("Helvetica", 12, "bold")
        )
```