import tkinter as tk
from tkinter import messagebox
import openai
import threading
import concurrent.futures
from utils.voice_manager import VoiceManager
from utils.gmail_manager import GmailManager
from utils.system_controller import SystemController
from utils.command_processor import CommandProcessor
from utils.gui_manager import GUIManager
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class REVA:
    def __init__(self):
        # Initialize OpenAI API Key securely
        self.openai = openai
        self.openai.api_key = os.getenv('')  # Fetch API key from .env
        if not self.openai.api_key:
            raise ValueError("OpenAI API key not found in environment variables. Check your .env file.")

        # Initialize components
        self.voice = VoiceManager()
        self.gmail = GmailManager()
        self.system = SystemController()
        self.command_processor = CommandProcessor(
            self.openai,
            self.voice,
            self.gmail,
            self.system
        )
        
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self.listening = True

    def start(self):
        root = tk.Tk()
        self.gui = GUIManager(root)
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start the listening loop in a separate thread
        self.thread = threading.Thread(target=self.listen_loop)
        self.thread.daemon = True
        self.thread.start()
        
        root.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.listening = False
            self.gui.master.destroy()

    def listen_loop(self):
        while self.listening:
            command = self.voice.listen()
            if command:
                self.gui.update_status(f"Processing: {command}")
                self.executor.submit(self.process_command, command)

    def process_command(self, command):
        try:
            success, message = self.command_processor.process_command(command)
            if not success:
                self.voice.say(f"Sorry, I couldn't complete that action: {message}", emotion="apologetic")
        except Exception as e:
            self.voice.say(f"An error occurred: {str(e)}", emotion="apologetic")
        finally:
            # Use Tkinter's thread-safe `after` method to update GUI
            self.gui.master.after(0, lambda: self.gui.update_status("Ready to assist..."))

if __name__ == "__main__":
    try:
        reva = REVA()
        reva.start()
    except Exception as e:
        print(f"Failed to start REVA: {str(e)}")
