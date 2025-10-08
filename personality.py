# personality.py
class NurAIPersonality:
    def __init__(self):
        self.name = "Nur AI"
        self.style = "lembut dan penuh hikmah"
        self.greetings = [
            "Assalamu'alaikum warahmatullahi wabarakatuh 🌙",
            "Selamat datang, saudaraku. Ada yang bisa Nur bantu?",
            "Salam sejahtera untukmu hari ini...",
        ]
    
    def get_greeting(self):
        import random
        return random.choice(self.greetings)
    
    def detect_emotion(self, text):
        text = text.lower()
        
        # Enhanced emotion keywords dengan intensity
        emotion_keywords = {
            "sedih": {
                "strong": ["putus asa", "patah hati", "menangis", "terluka", "kecewa banget"],
                "medium": ["sedih", "galau", "hati hancur", "sakit hati"],
                "weak": ["sedikit kecewa", "agak murung", "kurang semangat"]
            },
            "gelisah": {
                "strong": ["panik", "takut banget", "cemas berat", "gugup sekali"],
                "medium": ["gelisah", "khawatir", "cemas", "takut", "was-was"],
                "weak": ["agak khawatir", "sedikit cemas", "rada waspada"]
            },
            "bahagia": {
                "strong": ["sangat bahagia", "senang sekali", "alhamdulillah banget", "gembira luar biasa"],
                "medium": ["bahagia", "senang", "gembira", "alhamdulillah"],
                "weak": ["lumayan senang", "cukup bahagia", "agak gembira"]
            },
            "marah": {
                "strong": ["marah besar", "jengkel banget", "kesal sekali", "dendam"],
                "medium": ["marah", "kesal", "jengkel", "benci"],
                "weak": ["agak kesal", "sedikit jengkel", "rada marah"]
            },
            "bingung": {
                "strong": ["sangat bingung", "benar-benar bingung", "tak tahu arah", "kebingungan"],
                "medium": ["bingung", "ragu", "tak pasti", "dilema"],
                "weak": ["agak bingung", "sedikit ragu", "kurang yakin"]
            },
            "lelah": {
                "strong": ["sangat lelah", "capek banget", "tak berdaya", "kehabisan tenaga"],
                "medium": ["lelah", "capek", "penat", "letih"],
                "weak": ["agak lelah", "sedikit capek", "lumayan penat"]
            },
            "takut": {
                "strong": ["sangat takut", "ketakutan", "ngeri", "gentar"],
                "medium": ["takut", "khawatir", "cemas", "waspada"],
                "weak": ["agak takut", "sedikit khawatir", "rada waspada"]
            }
        }
        
        # Detect emotion dan intensity
        detected_emotion = "netral"
        intensity = "medium"
        
        for emotion, levels in emotion_keywords.items():
            for level, keywords in levels.items():
                if any(keyword in text for keyword in keywords):
                    detected_emotion = emotion
                    intensity = level
                    break
            if detected_emotion != "netral":
                break
        
        return {
            "emotion": detected_emotion,
            "intensity": intensity,
            "confidence": self._calculate_confidence(text, detected_emotion)
        }
    
    def _calculate_confidence(self, text, emotion):
        # Simple confidence calculation based on keyword matches
        if emotion == "netral":
            return 0.3
        
        emotion_words = [
            "sedih", "senang", "marah", "takut", "lelah", 
            "bingung", "gelisah", "bahagia", "cemas"
        ]
        
        matches = sum(1 for word in emotion_words if word in text)
        return min(0.3 + (matches * 0.2), 0.9)
