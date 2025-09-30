from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Chatbot:
    def __init__(self):
        # Try to initialize Gemini
        self.gemini_available = False
        self.gemini_model = None
        try:
            import google.generativeai as genai
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
                self.gemini_available = True
                print("Gemini AI integration enabled")
            else:
                print("Gemini API key not found, using fallback responses")
        except ImportError:
            print("Google Generative AI not available, using fallback responses")
        except Exception as e:
            print(
                f"Gemini initialization failed: {e}, using fallback responses")

        # Conversation storage for digital twin
        self.conversation_history = {}  # user_id -> list of conversation turns
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
            'help': 'Remember, it\'s okay to ask for help when you need it. I\'m here to support you.',
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
            
            message_lower = message.lower().strip()
            
            # Use multimodal emotion data if available
            multimodal_emotion = emotion.get('multimodal_emotion', emotion.get('label', 'neutral'))
            multimodal_confidence = emotion.get('multimodal_confidence', emotion.get('confidence', 0.5))
            
            # Adjust response based on emotion detection (lower threshold)
            if multimodal_confidence > 0.3:  # Lowered from 0.7
                if multimodal_emotion == 'sad' or 'sad' in message_lower or 'down' in message_lower or 'depressed' in message_lower:
                    response = "I can sense you're feeling down. Would you like to talk about what's bothering you?"
                    self._store_conversation(
                        user_id, message, response, emotion)
                    return response
                elif multimodal_emotion == 'anxious' or 'anxious' in message_lower or 'anxiety' in message_lower or 'worried' in message_lower:
                    response = "I hear that you're feeling anxious. Let's try some calming techniques together."
                    self._store_conversation(
                        user_id, message, response, emotion)
                    return response
                elif multimodal_emotion == 'angry' or 'angry' in message_lower or 'frustrated' in message_lower or 'upset' in message_lower:
                    response = "I hear frustration in your words. Can you tell me what's upsetting you?"
                    self._store_conversation(
                        user_id, message, response, emotion)
                    return response
                elif multimodal_emotion == 'happy' or 'happy' in message_lower or 'good' in message_lower or 'great' in message_lower:
                    response = "I can hear the positivity! That's wonderful. What's making you feel good?"
                    self._store_conversation(
                        user_id, message, response, emotion)
                    return response

            # Try Gemini AI response first if available
            gemini_response = self._generate_gemini_response(
                message, user_id, emotion, context)
            if gemini_response:
                # Store conversation for digital twin learning
                self._store_conversation(
                    user_id, message, gemini_response, emotion)
                return gemini_response

            # Enhanced keyword matching with more flexible patterns
            keyword_responses = {
                'hello': self.responses['hello'],
                'hi': self.responses['hello'],
                'hey': self.responses['hello'],
                'stressed': self.responses['stressed'],
                'stress': self.responses['stressed'],
                'tensed': self.responses['stressed'],
                'tense': self.responses['stressed'],
                'anxious': self.responses['anxious'],
                'anxiety': self.responses['anxious'],
                'worried': self.responses['anxious'],
                'sad': self.responses['sad'],
                'down': self.responses['sad'],
                'depressed': self.responses['sad'],
                'angry': self.responses['angry'],
                'mad': self.responses['angry'],
                'upset': self.responses['angry'],
                'frustrated': self.responses['angry'],
                'lonely': self.responses['lonely'],
                'alone': self.responses['lonely'],
                'tired': self.responses['tired'],
                'exhausted': self.responses['tired'],
                'sleep': "Getting enough sleep is crucial for mental health. How has your sleep been lately?",
                'exercise': "Regular physical activity can help improve your mood. Have you been able to exercise?",
                'breathe': "Try this breathing exercise: inhale for 4 counts, hold for 4, exhale for 4. Would you like me to guide you through it?",
                'help': self.responses['help'],
                'okay': "I understand. Sometimes it's hard to find the right words. I'm here whenever you're ready to talk.",
                'fine': "If you say you're fine, I'll believe you, but I'm here if you want to talk about anything.",
                'good': "That's good to hear! What made today good for you?",
                'bad': "I'm sorry to hear that. Would you like to talk about what's making things difficult?",
                'terrible': "That sounds really tough. I'm here to listen if you want to share.",
                'awful': "I'm sorry you're going through this. Your feelings are valid, and I'm here to support you.",
                'scared': "Feeling scared can be really overwhelming. What's frightening you right now?",
                'afraid': "It's okay to feel afraid sometimes. Can you tell me more about what's scaring you?",
                'overwhelmed': "Feeling overwhelmed is completely understandable. Let's break this down together.",
                'confused': "Confusion can be really unsettling. What feels unclear to you right now?",
                'lost': "Feeling lost is a common experience. I'm here to help you find your way.",
                'hopeless': "Even when things feel hopeless, there are always options and people who care. You're not alone.",
                'worthless': "You are absolutely not worthless. Your life has value, and there are people who care about you.",
                'useless': "That's not true at all. Everyone has worth and purpose. Let's talk about your strengths.",
                'hate': "Hate is a strong emotion. Can you tell me what's making you feel this way?",
                'hate myself': "I'm really concerned when I hear someone say they hate themselves. You deserve kindness and compassion.",
                'suicidal': "I'm really concerned about what you're saying. Your safety is the most important thing right now. Please reach out to emergency services immediately: National Suicide Prevention Lifeline: 988 (24/7)",
            }

            # Check for enhanced keywords
            for keyword, response in keyword_responses.items():
                if keyword in message_lower:
                    # Store conversation for digital twin learning
                    self._store_conversation(
                        user_id, message, response, emotion)
                    return response
            
            # Check for original keywords as fallback
            for key, response in self.responses.items():
                if key in message_lower and key != 'default':
                    # Store conversation for digital twin learning
                    self._store_conversation(
                        user_id, message, response, emotion)
                    return response
            
            # Try to get relevant info from knowledge base
            relevant_info = self._get_relevant_info(message_lower)
            if relevant_info:
                response = f"{self.responses['default']} {relevant_info}"
                # Store conversation for digital twin learning
                self._store_conversation(user_id, message, response, emotion)
                return response

            # Enhanced default responses based on message length and content
            if len(message_lower.split()) <= 2:  # Very short responses
                response = "I hear you. Can you tell me more about that?"
            elif '?' in message_lower:  # Questions
                response = "That's a good question. How are you feeling about it?"
            elif any(word in message_lower for word in ['feel', 'feeling', 'felt', 'feels']):
                response = "Thanks for sharing how you're feeling. Can you tell me more about what's causing that?"
            else:
                response = self.responses['default']
            
            # Store conversation for digital twin learning
            self._store_conversation(user_id, message, response, emotion)
            return response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, I'm having trouble processing your message right now. Please try again."
    
    def _get_relevant_info(self, message: str) -> str:
        """Get relevant information based on keywords in the message."""
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

    def _store_conversation(self, user_id: str, user_message: str, bot_response: str, emotion: Dict):
        """Store conversation for digital twin learning."""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []

        # Keep only last 20 conversations for memory efficiency
        if len(self.conversation_history[user_id]) >= 20:
            self.conversation_history[user_id] = self.conversation_history[user_id][-19:]

        self.conversation_history[user_id].append({
            'user_message': user_message,
            'bot_response': bot_response,
            'emotion': emotion.get('label', 'neutral'),
            'confidence': emotion.get('confidence', 0.5),
            'timestamp': str(__import__('time').time())
        })

    def _get_conversation_context(self, user_id: str, max_turns: int = 5) -> str:
        """Get recent conversation context for personalized responses."""
        if user_id not in self.conversation_history:
            return ""

        recent_conversations = self.conversation_history[user_id][-max_turns:]
        context_parts = []

        for conv in recent_conversations:
            context_parts.append(f"User: {conv['user_message']}")
            context_parts.append(f"Assistant: {conv['bot_response']}")

        return "\n".join(context_parts)

    def _generate_gemini_response(self, message: str, user_id: str, emotion: Dict, context: Optional[Dict] = None) -> Optional[str]:
        """Generate response using Gemini AI with conversation context."""
        try:
            if not self.gemini_available or not self.gemini_model:
                return None

            # Get conversation history
            conversation_context = self._get_conversation_context(user_id)

            # Build prompt with context
            system_prompt = """You are Aura, an empathetic AI mental health companion for youth. You provide supportive, understanding responses while being mindful of mental health best practices.

Key guidelines:
- Be empathetic and non-judgmental
- Encourage professional help when needed
- Focus on active listening and validation
- Provide practical coping strategies
- Recognize crisis signs and direct to appropriate resources
- Maintain appropriate boundaries as an AI companion

Current user emotion analysis: {emotion_label} (confidence: {emotion_confidence})

{conversation_context}

Respond to the user's message in a supportive, contextual way that considers their conversation history and current emotional state."""

            emotion_label = emotion.get('label', 'neutral')
            emotion_confidence = emotion.get('confidence', 0.5)

            prompt = system_prompt.format(
                emotion_label=emotion_label,
                emotion_confidence=f"{emotion_confidence:.2f}",
                conversation_context=f"Recent conversation:\n{conversation_context}" if conversation_context else "This is the start of the conversation."
            )

            # Add current message
            full_prompt = f"{prompt}\n\nUser: {message}\n\nAssistant:"

            response = self.gemini_model.generate_content(full_prompt)
            return response.text.strip()

        except Exception as e:
            print(f"Gemini API error: {e}")
            return None
