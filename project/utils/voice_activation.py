import speech_recognition as sr
import threading
import time

class VoiceActivationListener:
    def __init__(self, wake_word="hey reva", callback=None):
        self.wake_word = wake_word.lower()
        self.callback = callback
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.thread = None

    def start_listening(self):
        self.is_listening = True
        self.thread = threading.Thread(target=self._listen_loop)
        self.thread.daemon = True
        self.thread.start()

    def stop_listening(self):
        self.is_listening = False
        if self.thread:
            self.thread.join()

    def _listen_loop(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

        while self.is_listening:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    if self.wake_word in text:
                        if self.callback:
                            self.callback()
                        time.sleep(1)  # Prevent multiple activations
            except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
                continue