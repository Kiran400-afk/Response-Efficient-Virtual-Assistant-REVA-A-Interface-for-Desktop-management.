import tkinter as tk
from tkinter import ttk

class ModernStyle:
    # Colors
    PRIMARY_COLOR = "#007AFF"
    SECONDARY_COLOR = "#5856D6"
    BACKGROUND_COLOR = "#F5F5F7"
    SURFACE_COLOR = "#FFFFFF"
    TEXT_COLOR = "#1D1D1F"
    
    @staticmethod
    def apply_modern_style():
        style = ttk.Style()
        style.configure("Modern.TFrame", background=ModernStyle.BACKGROUND_COLOR)
        style.configure("Modern.TLabel",
                       background=ModernStyle.SURFACE_COLOR,
                       foreground=ModernStyle.TEXT_COLOR,
                       font=("Helvetica", 12))
        style.configure("Title.TLabel",
                       background=ModernStyle.SURFACE_COLOR,
                       foreground=ModernStyle.TEXT_COLOR,
                       font=("Helvetica", 16, "bold"))
        style.configure("Modern.TButton",
                       background=ModernStyle.PRIMARY_COLOR,
                       foreground="white",
                       padding=10)