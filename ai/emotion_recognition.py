from typing import Dict, Optional

class EmotionRecognition:
    def __init__(self):
        # Crisis detection keywords
        self.crisis_keywords = {
            'suicide': ['suicide', 'kill myself', 'end it all', 'not worth living', 'better off dead'],
            'self_harm': ['cut myself', 'hurt myself', 'self harm', 'self-harm', 'burn myself'],
            'emergency': ['emergency', 'crisis', 'help me now', 'i can\'t take it', 'breaking point'],
            'hopeless': ['no hope', 'hopeless', 'nothing matters', 'give up', 'end everything'],
            'panic': ['panic attack', 'can\'t breathe', 'heart racing', 'freaking out', 'losing control']
        }
        
        # Simple keyword-based emotion detection for demo
        self.emotion_keywords = {
            "sad": ["sad", "depressed", "unhappy", "down", "blue", "heartbroken", "lonely"],
            "anxious": ["anxious", "worried", "nervous", "scared", "fear", "panic", "stressed"],
            "angry": ["angry", "mad", "furious", "irritated", "annoyed", "frustrated"],
            "happy": ["happy", "joy", "excited", "great", "wonderful", "amazing", "good"],
            "tired": ["tired", "exhausted", "fatigued", "sleepy", "drained"],
            "confused": ["confused", "lost", "unsure", "bewildered", "puzzled"],
            "hopeful": ["hopeful", "optimistic", "positive", "encouraged"]
        }
        
        # Default emotion scores
        self.default_scores = {
            "sad": 0.0,
            "anxious": 0.0,
            "angry": 0.0,
            "happy": 0.0,
            "tired": 0.0,
            "confused": 0.0,
            "hopeful": 0.0
        }
    
    def detect_crisis(self, text: str) -> Optional[str]:
        """Detect if the text contains crisis-related keywords."""
        text_lower = text.lower()
        
        for crisis_type, keywords in self.crisis_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return crisis_type
        
        return None
    
    def analyze_text(self, text: str) -> Dict:
        try:
            text_lower = text.lower()
            scores = self.default_scores.copy()
            
            # Check for crisis first
            crisis_type = self.detect_crisis(text)
            
            # Count keyword matches
            for emotion, keywords in self.emotion_keywords.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        scores[emotion] += 0.2
            
            # Normalize scores
            total = sum(scores.values())
            if total > 0:
                for emotion in scores:
                    scores[emotion] /= total
            
            # Get top emotion
            top_emotion = max(scores.items(), key=lambda x: x[1])
            
            result = {
                "label": top_emotion[0] if top_emotion[1] > 0.1 else "neutral",
                "confidence": top_emotion[1] if top_emotion[1] > 0.1 else 0.5,
                "all_scores": scores
            }
            
            # Add crisis information if detected
            if crisis_type:
                result["crisis_detected"] = True
                result["crisis_type"] = crisis_type
                result["label"] = "crisis"
                result["confidence"] = 0.95
            
            return result
                
        except Exception as e:
            print(f"Error in emotion analysis: {e}")
            return {
                "label": "neutral",
                "confidence": 0.5,
                "all_scores": self.default_scores.copy()
            }
    
    def analyze_audio(self, audio_path: str) -> Dict:
        """Basic audio emotion analysis using librosa."""
        try:
            import librosa
            import numpy as np
            
            # Load audio file
            y, sr = librosa.load(audio_path, duration=30)  # Limit to 30 seconds
            
            # Extract basic audio features
            # Pitch/fundamental frequency
            f0 = librosa.yin(y, fmin=float(librosa.note_to_hz('C2')), fmax=float(librosa.note_to_hz('C7')))
            f0_mean = np.mean(f0[f0 > 0]) if np.any(f0 > 0) else 0
            
            # Energy/RMS
            rms = librosa.feature.rms(y=y)
            rms_mean = np.mean(rms)
            
            # Spectral centroid (brightness)
            centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
            centroid_mean = np.mean(centroid)
            
            # Zero crossing rate (noise vs tonal)
            zcr = librosa.feature.zero_crossing_rate(y)
            zcr_mean = np.mean(zcr)
            
            # Simple emotion classification based on audio features
            emotion = "neutral"
            confidence = 0.5
            
            # High pitch + high energy = excited/happy
            if f0_mean > 200 and rms_mean > 0.1:
                emotion = "excited"
                confidence = 0.7
            # Low pitch + low energy = sad/depressed
            elif f0_mean < 150 and rms_mean < 0.05:
                emotion = "sad"
                confidence = 0.6
            # High zero crossing + high energy = anxious/stressed
            elif zcr_mean > 0.1 and rms_mean > 0.08:
                emotion = "anxious"
                confidence = 0.65
            
            return {
                "emotion": emotion,
                "confidence": confidence,
                "features": {
                    "pitch_mean": float(f0_mean),
                    "energy_mean": float(rms_mean),
                    "centroid_mean": float(centroid_mean),
                    "zcr_mean": float(zcr_mean)
                }
            }
            
        except Exception as e:
            print(f"Error in audio analysis: {e}")
            return {
                "emotion": "neutral",
                "confidence": 0.5,
                "error": str(e)
            }
    
    def analyze_video(self, video_path: str) -> Dict:
        """Basic video emotion analysis placeholder."""
        try:
            import cv2
            import numpy as np
            
            # Open video file
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                return {"emotion": "neutral", "confidence": 0.5, "error": "Could not open video file"}
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            
            # Sample frames (every 1 second)
            emotions = []
            frame_interval = int(fps) if fps > 0 else 30
            
            for i in range(0, min(frame_count, int(duration * fps)), frame_interval):
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                
                if ret:
                    # Convert to grayscale for basic analysis
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    
                    # Simple brightness analysis (placeholder for facial emotion)
                    brightness = np.mean(gray) / 255.0
                    
                    # Very basic emotion inference from brightness
                    if brightness > 0.6:
                        emotions.append("happy")
                    elif brightness < 0.4:
                        emotions.append("sad")
                    else:
                        emotions.append("neutral")
            
            cap.release()
            
            # Get most common emotion
            if emotions:
                from collections import Counter
                most_common = Counter(emotions).most_common(1)[0]
                emotion = most_common[0]
                confidence = most_common[1] / len(emotions)
            else:
                emotion = "neutral"
                confidence = 0.5
            
            return {
                "emotion": emotion,
                "confidence": confidence,
                "video_info": {
                    "duration": duration,
                    "fps": fps,
                    "frames_analyzed": len(emotions)
                }
            }
            
        except Exception as e:
            print(f"Error in video analysis: {e}")
            return {
                "emotion": "neutral",
                "confidence": 0.5,
                "error": str(e)
            }
    
    def analyze_multimodal(self, text: str, audio_path: Optional[str] = None, image_path: Optional[str] = None) -> Dict:
        """Analyze text, audio, and video for comprehensive emotion detection."""
        # Start with text analysis
        result = self.analyze_text(text)
        
        # Analyze audio if provided
        if audio_path:
            audio_result = self.analyze_audio(audio_path)
            result["audio_analysis"] = audio_result
            
            # Combine emotions (simple weighted average)
            if audio_result["confidence"] > 0.6:
                # If audio confidence is high, adjust overall emotion
                if audio_result["emotion"] != result["label"]:
                    result["multimodal_emotion"] = audio_result["emotion"]
                    result["multimodal_confidence"] = (result["confidence"] + audio_result["confidence"]) / 2
                else:
                    result["multimodal_confidence"] = max(result["confidence"], audio_result["confidence"])
        
        # Analyze video if provided
        if image_path:
            # For now, treat image as single frame video
            video_result = self.analyze_video(image_path)
            result["video_analysis"] = video_result
            
            # Combine with existing analysis
            if video_result["confidence"] > 0.6:
                if "multimodal_emotion" in result:
                    # Average all three modalities
                    result["final_emotion"] = result["multimodal_emotion"]
                    result["final_confidence"] = (result["multimodal_confidence"] + video_result["confidence"]) / 2
                else:
                    result["multimodal_emotion"] = video_result["emotion"]
                    result["multimodal_confidence"] = (result["confidence"] + video_result["confidence"]) / 2
        
        return result