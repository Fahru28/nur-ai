# personality_enhanced.py
class EnhancedNurAIPersonality:
    def __init__(self):
        self.name = "Nur AI"
        self.style = "lembut dan penuh hikmah"
    
    def detect_emotion_and_intent(self, text):
        text = text.lower()
        
        # Intent detection
        intents = {
            "request_quotes": any(word in text for word in ["quotes", "kutipan", "kata bijak", "motivasi", "inspirasi"]),
            "request_verse": any(word in text for word in ["ayat", "quran", "al-quran", "firman"]),
            "request_prayer": any(word in text for word in ["doa", "pray", "doakan"]),
            "request_advice": any(word in text for word in ["nasehat", "saran", "masukan", "sarankan"]),
            "greeting": any(word in text for word in ["hai", "halo", "hello", "assalamu'alaikum", "selamat"]),
            "confused": any(word in text for word in ["apa ya", "bingung", "gimana", "bagaimana", "tidak tahu"])
        }
        
        # Emotion detection (improved)
        emotion_keywords = {
            "sedih": ["sedih", "kecewa", "menangis", "putus asa", "patah hati"],
            "gelisah": ["cemas", "khawatir", "takut", "gelisah", "was-was"],
            "bahagia": ["senang", "bahagia", "syukur", "alhamdulillah", "gembira"],
            "marah": ["marah", "kesal", "jengkel", "dendam", "benci"],
            "bingung": ["bingung", "ragu", "tidak tahu", "pusing", "dilema", "apa ya"],
            "lelah": ["lelah", "capek", "penat", "letih"],
            "takut": ["takut", "khawatir", "cemas", "gentar"]
        }
        
        detected_emotion = "netral"
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text for keyword in keywords):
                detected_emotion = emotion
                break
        
        # Determine primary intent
        primary_intent = "chat"
        for intent, detected in intents.items():
            if detected:
                primary_intent = intent
                break
        
        return {
            "emotion": detected_emotion,
            "intent": primary_intent,
            "text": text
        }
