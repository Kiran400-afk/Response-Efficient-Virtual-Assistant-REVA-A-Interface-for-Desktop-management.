from typing import Dict, List
import random

class VoiceExpressions:
    def __init__(self):
        self.expressions: Dict[str, List[str]] = {
            'greeting': [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Greetings! How may I assist you?"
            ],
            'thinking': [
                "Let me think about that...",
                "Processing your request...",
                "Analyzing that information..."
            ],
            'confirmation': [
                "I've completed your request.",
                "That's done for you.",
                "All set!"
            ],
            'error': [
                "I apologize, but I encountered an error.",
                "Sorry, something went wrong.",
                "I couldn't complete that action."
            ],
            'farewell': [
                "Goodbye! Have a great day!",
                "See you later!",
                "Until next time!"
            ]
        }
    
    def get_expression(self, category: str) -> str:
        
        if category in self.expressions:
            return random.choice(self.expressions[category])
        return ""
