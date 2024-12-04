import pyttsx3
import speech_recognition as sr
from typing import Optional, Tuple
import threading
from queue import Queue
from .voice_expressions import VoiceExpressions

class VoiceProperties:
    def __init__(self):
        self.rate = 175  # Default speech rate
        self.volume = 1.0  # Default volume
        self.pitch = 1.0  # Default pitch

class VoiceManager:
    def __init__(self, voice_type: str = 'female'):
        self.engine = pyttsx3.init()
        self.voice_properties = VoiceProperties()
        self.expressions = VoiceExpressions()
        self.speech_queue = Queue()
        self.setup_voice(voice_type)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Start speech processing thread
        self.speech_thread = threading.Thread(target=self._process_speech_queue, daemon=True)
        self.speech_thread.start()

    def setup_voice(self, voice_type: str):
        
        voices = self.engine.getProperty('voices')
        
        # Find the most natural-sounding female voice
        selected_voice = None
        for voice in voices:
            if voice_type in voice.name.lower() and ('natural' in voice.name.lower() or 
                                                   'premium' in voice.name.lower() or 
                                                   'enhanced' in voice.name.lower()):
                selected_voice = voice
                break
        
        # If no enhanced voice found, use the first female voice
        if not selected_voice:
            for voice in voices:
                if voice_type in voice.name.lower():
                    selected_voice = voice
                    break

        if selected_voice:
            self.engine.setProperty('voice', selected_voice.id)

        # Set natural-sounding properties
        self.engine.setProperty('rate', self.voice_properties.rate)
        self.engine.setProperty('volume', self.voice_properties.volume)

    def _process_speech_queue(self):
        
        while True:
            text, properties = self.speech_queue.get()
            self._apply_properties(properties)
            self.engine.say(text)
            self.engine.runAndWait()
            self.speech_queue.task_done()

    def _apply_properties(self, properties: VoiceProperties):
        
        self.engine.setProperty('rate', properties.rate)
        self.engine.setProperty('volume', properties.volume)

    def say(self, text: str, emotion: str = None):
        
        if emotion:
            text = self.expressions.add_expression_to_response(text, emotion)

        # Create temporary properties for this speech
        properties = VoiceProperties()
        
        # Adjust properties based on emotion
        if emotion == 'happy':
            properties.rate = 185
            properties.pitch = 1.1
        elif emotion == 'apologetic':
            properties.rate = 165
            properties.pitch = 0.9
        elif emotion == 'thinking':
            properties.rate = 160
            properties.pitch = 1.0

        # Add to speech queue
        self.speech_queue.put((text, properties))

    def listen(self, timeout: int = 5, phrase_time_limit: int = 5) -> Optional[str]:
        
        with self.microphone as source:
            # Dynamic noise adjustment
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                # Use multiple recognition engines for better accuracy
                try:
                    return self.recognizer.recognize_google(audio)
                except:
                    try:
                        return self.recognizer.recognize_sphinx(audio)
                    except:
                        return None
                        
            except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
                return None

    def adjust_voice(self, rate: int = None, volume: float = None, pitch: float = None):
        
        if rate is not None:
            self.voice_properties.rate = max(50, min(300, rate))
        if volume is not None:
            self.voice_properties.volume = max(0.1, min(1.0, volume))
        if pitch is not None:
            self.voice_properties.pitch = max(0.5, min(2.0, pitch))
