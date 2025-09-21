from typing import Dict, Any, Optional

class Chatbot:
    def __init__(self):
        # Crisis detection keywords
        self.crisis_keywords = {
            'suicide': ['suicide', 'kill myself', 'end it all', 'not worth living', 'better off dead'],
            'self_harm': ['cut myself', 'hurt myself', 'self harm', 'self-harm', 'burn myself'],
            'emergency': ['emergency', 'crisis', 'help me now', 'i can\'t take it', 'breaking point'],
            'hopeless': ['no hope', 'hopeless', 'nothing matters', 'give up', 'end everything'],
            'panic': ['panic attack', 'can\'t breathe', 'heart racing', 'freaking out', 'losing control']
        }
        
        # Crisis response templates
        self.crisis_responses = {
            'immediate_help': "I'm really concerned about what you're saying. Your safety is the most important thing right now. Please reach out to emergency services immediately:",
            'hotlines': {
                'us': "National Suicide Prevention Lifeline: 988 (24/7)",
                'uk': "Samaritans: 116 123 (24/7)",
                'canada': "Canada Suicide Prevention Service: 988",
                'australia': "Lifeline: 13 11 14 (24/7)",
                'international': "Find local crisis support at befrienders.org"
            },
            'resources': [
                "You are not alone in this",
                "Your feelings are valid, but this pain can be temporary",
                "Professional help can make a real difference",
                "There are people who care about you and want to help"
            ]
        }
        
        # Simple responses for demo
        self.responses = {
            'hello': 'Hello! How can I help you today?',
            'sad': 'I\'m sorry you\'re feeling sad. Would you like to talk about what\'s bothering you?',
            'anxious': 'Anxiety can be tough. Let\'s try some deep breathing exercises together.',
            'happy': 'That\'s great! What\'s making you feel happy?',
            'angry': 'I hear that you\'re feeling angry. Can you tell me more about what\'s upsetting you?',
            'stressed': 'Stress can be overwhelming. What\'s causing you the most stress right now?',
            'lonely': 'Feeling lonely is really hard. Remember that you\'re not alone - I\'m here to listen.',
            'tired': 'Being tired can affect everything. Have you been getting enough rest?',
            'default': 'I\'m here to listen. Can you tell me more about how you\'re feeling?'
        }
        
        # Knowledge base for RAG-like responses
        self.knowledge_base = [
            "Practice deep breathing: inhale for 4 counts, hold for 4, exhale for 4.",
            "Talking to someone you trust can help lighten your emotional load.",
            "Regular exercise can boost your mood and reduce stress.",
            "Getting 7-9 hours of sleep is important for mental health.",
            "Writing down your thoughts in a journal can help process emotions.",
            "Mindfulness meditation can help you stay present and reduce anxiety.",
            "It's okay to ask for help - reaching out is a sign of strength.",
            "Setting small, achievable goals can build confidence over time.",
            "Staying connected with supportive people is important for well-being.",
            "Professional help is always available through therapists and counselors."
        ]
    
    def _detect_crisis(self, message: str) -> Optional[str]:
        """Detect crisis keywords in the message."""
        message_lower = message.lower()
        
        for crisis_type, keywords in self.crisis_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return crisis_type
        
        return None
    
    def _generate_crisis_response(self, crisis_type: str) -> str:
        """Generate appropriate crisis response."""
        response_parts = []
        
        # Immediate help message
        response_parts.append(self.crisis_responses['immediate_help'])
        
        # Add relevant hotline based on crisis type
        if crisis_type in ['suicide', 'self_harm']:
            response_parts.append("🚨 IMMEDIATE HELP NEEDED:")
            response_parts.append("• US: National Suicide Prevention Lifeline - Call or text 988")
            response_parts.append("• UK: Samaritans - Call 116 123")
            response_parts.append("• Canada: Canada Suicide Prevention Service - Call 988")
            response_parts.append("• Australia: Lifeline - Call 13 11 14")
            response_parts.append("• International: Find local support at befrienders.org")
        
        # Add supportive resources
        response_parts.append("\nYou are not alone. These feelings can be overwhelming, but help is available:")
        for resource in self.crisis_responses['resources']:
            response_parts.append(f"• {resource}")
        
        response_parts.append("\nPlease reach out to these services right now. Your life matters.")
        
        return "\n".join(response_parts)
    
    async def generate_response(self, message: str, user_id: str, emotion: Dict, context: Optional[Dict] = None) -> str:
        try:
            # First, check for crisis keywords
            crisis_type = self._detect_crisis(message)
            if crisis_type:
                return self._generate_crisis_response(crisis_type)
            
            message_lower = message.lower()
            
            # Use multimodal emotion data if available
            multimodal_emotion = emotion.get('multimodal_emotion', emotion.get('label', 'neutral'))
            multimodal_confidence = emotion.get('multimodal_confidence', emotion.get('confidence', 0.5))
            
            # Adjust response based on multimodal emotion detection
            if multimodal_confidence > 0.7:
                # High confidence multimodal detection
                if multimodal_emotion == 'sad':
                    return "I can sense you're feeling down through your words and tone. Would you like to talk about what's bothering you?"
                elif multimodal_emotion == 'anxious':
                    return "Your voice and words suggest you're feeling anxious. Let's try some calming techniques together."
                elif multimodal_emotion == 'angry':
                    return "I hear frustration in your voice. Can you tell me what's upsetting you?"
                elif multimodal_emotion == 'happy':
                    return "I can hear the positivity in your voice! That's wonderful. What's making you feel good?"
            
            # Check for keywords
            for key, response in self.responses.items():
                if key in message_lower and key != 'default':
                    return response
            
            # Default response with some relevant info
            base_response = self.responses['default']
            
            # Add relevant knowledge
            relevant_info = self._get_relevant_info(message_lower)
            if relevant_info:
                return f"{base_response} {relevant_info}"
            
            return base_response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, I'm having trouble processing your message right now. Please try again."
    
    def _get_relevant_info(self, message: str) -> str:
        # Simple keyword matching for demo
        keywords = {
            'sleep': "Getting enough sleep is crucial for mental health.",
            'exercise': "Regular physical activity can help improve your mood.",
            'breathe': "Try this breathing exercise: inhale for 4, hold for 4, exhale for 4.",
            'help': "Remember, it's okay to ask for help when you need it.",
            'stress': "When stressed, try to break down tasks into smaller steps.",
            'anxiety': "For anxiety, grounding techniques like naming 5 things you can see can help.",
            'sad': "It's normal to feel sad sometimes. Talking about it can help.",
            'happy': "That's wonderful! What makes you feel happy?",
            'friend': "Having supportive friends is so important for mental health."
        }
        
        for keyword, info in keywords.items():
            if keyword in message:
                return info
        
        return ""