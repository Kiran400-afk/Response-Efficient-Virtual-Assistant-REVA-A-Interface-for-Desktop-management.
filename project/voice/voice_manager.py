import pyttsx3
import speech_recognition as sr
from typing import Optional
import threading
from queue import Queue
from config import VOICE_TYPE, VOICE_RATE, VOICE_VOLUME

class VoiceManager:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.setup_voice()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.speech_queue = Queue()
        
        # Start speech processing thread
        self.speech_thread = threading.Thread(target=self._process_speech_queue, daemon=True)
        self.speech_thread.start()

    def setup_voice(self):
        
        voices = self.engine.getProperty('voices')
        # Select female voice
        for voice in voices:
            if VOICE_TYPE in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        self.engine.setProperty('rate', VOICE_RATE)
        self.engine.setProperty('volume', VOICE_VOLUME)

    def _process_speech_queue(self):
        
        while True:
            text = self.speech_queue.get()
            self.engine.say(text)
            self.engine.runAndWait()
            self.speech_queue.task_done()

    def say(self, text: str):
        
        self.speech_queue.put(text)

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
