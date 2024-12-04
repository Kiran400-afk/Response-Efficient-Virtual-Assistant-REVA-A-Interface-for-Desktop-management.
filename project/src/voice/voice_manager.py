import pyttsx3
import speech_recognition as sr
from typing import Optional

class VoiceManager:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.setup_voice()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def setup_voice(self):
        voices = self.engine.getProperty('voices')
        # Find and set female voice
        for voice in voices:
            if 'female' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Set natural-sounding properties
        self.engine.setProperty('rate', 175)  # Speed
        self.engine.setProperty('volume', 1.0)  # Volume

    def say(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, timeout: int = 5, phrase_time_limit: int = 5) -> Optional[str]:
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                return self.recognizer.recognize_google(audio)
            except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
                return None