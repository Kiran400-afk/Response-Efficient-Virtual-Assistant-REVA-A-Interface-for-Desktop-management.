from typing import Dict, Any, Tuple
import re
from .system_controller import SystemController
import openai

class CommandProcessor:
    def __init__(self, openai_client, voice_manager, gmail_manager, system_controller):
        self.openai = openai_client
        self.voice = voice_manager
        self.gmail = gmail_manager
        self.system = system_controller

    def process_command(self, command: str):
        command = command.lower()
        
        try:
            # Email commands
            if "send email" in command:
                return self.handle_email_command(command)
            
            # System control commands
            elif any(word in command for word in ["open", "launch", "start"]):
                return self.handle_system_command(command)
            
            # Website commands
            elif "go to" in command or "visit" in command:
                return self.handle_website_command(command)
            
            # Volume control
            elif "volume" in command:
                return self.handle_volume_command(command)
            
            # Brightness control
            elif "brightness" in command:
                return self.handle_brightness_command(command)
            
            # Default to ChatGPT
            else:
                return self.handle_chat_command(command)
                
        except Exception as e:
            self.voice.say(f"Sorry, I encountered an error: {str(e)}", emotion="apologetic")
            return False, str(e)

    def handle_email_command(self, command) -> Tuple[bool, str]:
        response = self.openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Extract email details from the command in JSON format with 'to', 'subject', and 'message' fields."},
                {"role": "user", "content": command}
            ]
        )
        
        email_details = eval(response.choices[0].message.content)
        success = self.gmail.send_email(
            email_details['to'],
            email_details['subject'],
            email_details['message']
        )
        
        message = "Email sent successfully!" if success else "Failed to send email."
        self.voice.say(message, emotion="happy" if success else "apologetic")
        return success, message

    def handle_system_command(self, command) -> Tuple[bool, str]:
        for app in self.system.OFFICE_APPS:
            if app in command:
                success, message = self.system.open_office_app(app)
                self.voice.say(message, emotion="happy" if success else "apologetic")
                return success, message
        return False, "No matching application found"

    def handle_website_command(self, command) -> Tuple[bool, str]:
        for site in self.system.WEBSITES:
            if site in command:
                success, message = self.system.open_website(site)
                self.voice.say(message, emotion="happy" if success else "apologetic")
                return success, message
        return False, "Website not recognized"

    def handle_volume_command(self, command) -> Tuple[bool, str]:
        if "mute" in command:
            success, message = self.system.control_volume(mute=True)
        elif "unmute" in command:
            success, message = self.system.control_volume(mute=False)
        else:
            match = re.search(r'(\d+)', command)
            if match:
                level = int(match.group(1))
                success, message = self.system.control_volume(level=level)
            else:
                success, message = False, "Could not determine volume level"
        
        self.voice.say(message, emotion="happy" if success else "apologetic")
        return success, message

    def handle_brightness_command(self, command) -> Tuple[bool, str]:
        match = re.search(r'(\d+)', command)
        if match:
            level = int(match.group(1))
            success, message = self.system.set_brightness(level)
            self.voice.say(message, emotion="happy" if success else "apologetic")
            return success, message
        
        self.voice.say("Could not determine brightness level", emotion="apologetic")
        return False, "Could not determine brightness level"

    def handle_chat_command(self, command) -> Tuple[bool, str]:
        response = self.openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are REVA, a helpful desktop assistant."},
                {"role": "user", "content": command}
            ]
        )
        message = response.choices[0].message.content
        self.voice.say(message)
        return True, message
