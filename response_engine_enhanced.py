# response_engine_enhanced.py
from personality_enhanced import EnhancedNurAIPersonality
from knowledge.islamic_knowledge import IslamicKnowledge
import random
from datetime import datetime

class EnhancedResponseEngine:
    def __init__(self):
        self.personality = EnhancedNurAIPersonality()
        self.knowledge = IslamicKnowledge()
        
        # Pre-load quick responses
        self._preload_quick_responses()
    
    def _preload_quick_responses(self):
        self.quick_quotes = [
            "Hati yang tenang adalah taman yang subur untuk iman tumbuh.",
            "Kesabaran itu seperti pohon, akarnya pahit tapi buahnya manis.",
            "Bersyukurlah dalam segala keadaan, karena setiap napas adalah anugerah.",
            "Ketika doa-doa tertunda, percayalah bahwa Allah sedang menyiapkan yang terbaik.",
            "Dunia ini hanya jembatan, maka seberangilah jembatan itu dan jangan menjadikannya tempat tinggal.",
            "Ketenangan hati tidak diukur dari banyaknya harta, tapi dari cukupnya rasa syukur."
        ]
        
        self.greeting_responses = [
            "Assalamu'alaikum! Senang sekali mendengar sapaan darimu 🌙",
            "Wa'alaikumussalam warahmatullahi wabarakatuh! Ada cerita apa hari ini?",
            "Alhamdulillah, senang berbicara denganmu! Apa kabar hari ini?",
            "Salam sejahtera untukmu! Ceritakan apa yang membuatmu tersenyum hari ini...",
            "Hai! Semoga harimu penuh berkah dan ketenangan 💫"
        ]
        
        self.confused_responses = [
            "Wah, sepertinya ada yang sedang membuatmu bingung. Mari kita cari kejelasan bersama...",
            "Kebingungan adalah kesempatan untuk belajar. Apa yang membuatmu penasaran?",
            "Mari kita eksplorasi bersama, mungkin aku bisa membantu memberikan perspektif...",
            "Setiap kebingungan ada hikmahnya. Ceritakan apa yang ingin kamu pahami...",
            "Aku di sini untuk membantu. Apa yang sedang kamu pikirkan?"
        ]

    def generate_response(self, user_input):
        # Detect emotion and intent
        analysis = self.personality.detect_emotion_and_intent(user_input)
        emotion = analysis["emotion"]
        intent = analysis["intent"]
        
        # Handle specific intents first
        if intent == "request_quotes":
            return self._handle_quotes_request()
        elif intent == "greeting":
            return self._handle_greeting()
        elif intent == "confused":
            return self._handle_confused()
        elif intent == "request_verse":
            return self._handle_verse_request()
        elif intent == "request_prayer":
            return self._handle_prayer_request()
        elif intent == "request_advice":
            return self._handle_advice_request()
        else:
            return self._handle_general_chat(emotion, user_input)
    
    def _handle_quotes_request(self):
        quote = random.choice(self.quick_quotes)
        return {
            "response": f"💫 {quote}\n\nMau quotes lainnya atau ada yang ingin diceritakan?",
            "emotion": "inspirational",
            "timestamp": datetime.now().strftime("%H:%M")
        }
    
    def _handle_greeting(self):
        greeting = random.choice(self.greeting_responses)
        return {
            "response": greeting,
            "emotion": "welcoming", 
            "timestamp": datetime.now().strftime("%H:%M")
        }
    
    def _handle_confused(self):
        response = random.choice(self.confused_responses)
        return {
            "response": response,
            "emotion": "supportive",
            "timestamp": datetime.now().strftime("%H:%M")
        }
    
    def _handle_verse_request(self):
        verse = random.choice(self.knowledge.quran_verses)
        return {
            "response": f"📖 {verse['text']}\n— {verse['ayat']}\n\nMau ayat dengan tema tertentu?",
            "emotion": "spiritual",
            "timestamp": datetime.now().strftime("%H:%M")
        }
    
    def _handle_prayer_request(self):
        prayer = self.knowledge.get_daily_prayer()
        return {
            "response": f"🤲 {prayer}\n\nAmin ya Rabbal 'alamin...",
            "emotion": "prayerful",
            "timestamp": datetime.now().strftime("%H:%M")
        }
    
    def _handle_advice_request(self):
        wisdom = random.choice(self.knowledge.wisdom_quotes)
        return {
            "response": f"💡 {wisdom}\n\nMau saran tentang hal spesifik?",
            "emotion": "wise",
            "timestamp": datetime.now().strftime("%H:%M")
        }
    
    def _handle_general_chat(self, emotion, user_input):
        # Default responses based on emotion
        emotion_responses = {
            "sedih": "Wahai saudaraku, janganlah bersedih. Allah dekat dengan orang yang patah hati...",
            "gelisah": "Tenanglah, hanya dengan mengingat Allah hati menjadi tenteram...", 
            "bahagia": "Alhamdulillah! Senang mendengar kabar baikmu...",
            "bingung": "Mari kita cari kejelasan bersama...",
            "netral": "Ceritakan lebih banyak, aku sungguh-sungguh mendengarkan..."
        }
        
        response = emotion_responses.get(emotion, emotion_responses["netral"])
        
        # Add some variety
        if random.random() > 0.7:  # 30% chance to add wisdom
            wisdom = random.choice(self.quick_quotes)
            response += f"\n\n💫 {wisdom}"
        
        return {
            "response": response,
            "emotion": emotion,
            "timestamp": datetime.now().strftime("%H:%M")
        }

# Test the enhanced engine
if __name__ == "__main__":
    engine = EnhancedResponseEngine()
    
    test_inputs = [
        "Hai",
        "Kasih quotes dong", 
        "Apa ya",
        "Beri aku motivasi",
        "Bacakan ayat Quran"
    ]
    
    for test in test_inputs:
        result = engine.generate_response(test)
        print(f"Input: '{test}'")
        print(f"Intent: {result['emotion']}")
        print(f"Response: {result['response']}")
        print("-" * 60)
