from typing import Dict, List
import random

class VoiceExpressions:
    def __init__(self):
        self.expressions: Dict[str, List[str]] = {
            'happy': [
                'That makes me happy!',
                'I\'m glad I could help!',
                'Wonderful!',
                'That\'s great news!'
            ],
            'thinking': [
                'Let me think about that...',
                'Processing that request...',
                'Give me a moment...',
                'Analyzing that information...'
            ],
            'apologetic': [
                'I apologize for that.',
                'I\'m sorry, let me try again.',
                'That didn\'t work as expected, sorry.',
                'My apologies for the confusion.'
            ],
            'encouraging': [
                'You\'re doing great!',
                'Let\'s try that!',
                'That\'s a good approach!',
                'We can definitely handle that!'
            ]
        }
        
    def get_expression(self, emotion: str) -> str:
        
        if emotion in self.expressions:
            return random.choice(self.expressions[emotion])
        return ''

    def add_expression_to_response(self, response: str, emotion: str) -> str:
        
        expression = self.get_expression(emotion)
        if expression:
            return f"{expression} {response}"
        return response
