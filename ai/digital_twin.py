from typing import Dict, List, Any
from datetime import datetime, timedelta
import asyncio

class DigitalTwin:
    def __init__(self):
        self.user_profiles = {}
        self.prediction_model = self._load_prediction_model()
    
    def _load_prediction_model(self):
        # Simple prediction model (placeholder)
        # In full implementation, would use ML model for predictions
        return {
            "mood_trends": [],
            "risk_factors": []
        }
    
    async def update_profile(self, user_id: str, data: Dict[str, Any]):
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                "user_id": user_id,
                "created_at": datetime.now(),
                "interactions": [],
                "mood_history": [],
                "risk_assessment": "low",
                "last_interaction": None
            }
        
        profile = self.user_profiles[user_id]
        
        # Add timestamp
        data["timestamp"] = datetime.now()
        
        # Update interactions
        profile["interactions"].append(data)
        profile["last_interaction"] = data["timestamp"]
        
        # Update mood history
        if "emotion" in data:
            profile["mood_history"].append({
                "emotion": data["emotion"],
                "timestamp": data["timestamp"],
                "message": data.get("message", "")
            })
        
        # Keep only last 100 interactions
        if len(profile["interactions"]) > 100:
            profile["interactions"] = profile["interactions"][-100:]
        
        # Update risk assessment
        profile["risk_assessment"] = self._assess_risk(profile)
    
    def _assess_risk(self, profile: Dict) -> str:
        # Simple risk assessment based on recent interactions
        recent_interactions = profile["interactions"][-10:]  # Last 10 interactions
        
        negative_emotions = ["sad", "angry", "anxious", "fear"]
        negative_count = sum(1 for interaction in recent_interactions 
                           if interaction.get("emotion") in negative_emotions)
        
        if negative_count >= 7:
            return "high"
        elif negative_count >= 4:
            return "medium"
        else:
            return "low"
    
    async def get_profile(self, user_id: str) -> Dict:
        return self.user_profiles.get(user_id, {})
    
    async def predict_mood(self, user_id: str) -> Dict:
        profile = self.user_profiles.get(user_id, {})
        if not profile or not profile["mood_history"]:
            return {"prediction": "neutral", "confidence": 0.5}
        
        # Simple prediction based on recent mood
        recent_moods = profile["mood_history"][-5:]
        mood_counts = {}
        
        for mood_entry in recent_moods:
            emotion = mood_entry["emotion"]
            mood_counts[emotion] = mood_counts.get(emotion, 0) + 1
        
        predicted_mood = max(mood_counts.keys(), key=lambda x: mood_counts[x])
        confidence = mood_counts[predicted_mood] / len(recent_moods)
        
        return {
            "prediction": predicted_mood,
            "confidence": confidence,
            "based_on": len(recent_moods)
        }
    
    async def get_insights(self, user_id: str) -> Dict:
        profile = self.user_profiles.get(user_id, {})
        
        if not profile:
            return {"insights": "No data available"}
        
        insights = {
            "total_interactions": len(profile["interactions"]),
            "risk_level": profile["risk_assessment"],
            "most_common_emotion": self._get_most_common_emotion(profile),
            "activity_trend": self._get_activity_trend(profile),
            "recommendations": self._generate_recommendations(profile)
        }
        
        return insights
    
    def _get_most_common_emotion(self, profile: Dict) -> str:
        emotions = [interaction.get("emotion") for interaction in profile["interactions"] 
                   if interaction.get("emotion")]
        
        if not emotions:
            return "neutral"
        
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        return max(emotion_counts.keys(), key=lambda x: emotion_counts[x])
    
    def _get_activity_trend(self, profile: Dict) -> str:
        interactions = profile["interactions"]
        if len(interactions) < 7:
            return "insufficient_data"
        
        # Check last 7 days activity
        last_week = datetime.now() - timedelta(days=7)
        recent_count = sum(1 for interaction in interactions 
                          if interaction.get("timestamp", datetime.min) > last_week)
        
        if recent_count >= 5:
            return "active"
        elif recent_count >= 2:
            return "moderate"
        else:
            return "low"
    
    def _generate_recommendations(self, profile: Dict) -> List[str]:
        recommendations = []
        
        risk = profile["risk_assessment"]
        if risk == "high":
            recommendations.append("Consider speaking with a mental health professional")
            recommendations.append("Reach out to crisis hotline if needed")
        
        activity = self._get_activity_trend(profile)
        if activity == "low":
            recommendations.append("Try to engage more regularly with the app")
        
        most_common = self._get_most_common_emotion(profile)
        if most_common in ["sad", "anxious"]:
            recommendations.append("Consider mindfulness exercises or breathing techniques")
        
        return recommendations