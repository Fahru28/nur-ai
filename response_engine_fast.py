# response_engine_fast.py - Optimized for speed
from personality import NurAIPersonality
from knowledge.islamic_knowledge import IslamicKnowledge
import random
from datetime import datetime

class FastResponseEngine:
    def __init__(self):
        self.personality = NurAIPersonality()
        self.knowledge = IslamicKnowledge()
        
        # Pre-load responses for faster access
        self._preload_responses()
    
    def _preload_responses(self):
        """Pre-load responses untuk akses lebih cepat"""
        self.quick_responses = {
            "sedih": [
                "Wahai saudaraku, jangan bersedih. Allah dekat dengan orang yang patah hati...",
                "Setiap kesedian ada hikmahnya. Mari kita ingat bersama kebesaran Allah...",
                "Jangan putus asa dari rahmat Allah. Setiap kesulitan pasti ada kemudahan..."
            ],
            "gelisah": [
                "Tenanglah, hanya dengan mengingat Allah hati menjadi tenteram...",
                "Mari tarik napas dalam dan serahkan semua pada Allah...",
                "Kegelisahan akan berlalu dengan dzikir dan tawakal..."
            ],
            "bahagia": [
                "Alhamdulillah! Syukuri kebahagiaan ini dengan berbagi kebaikan...",
                "Senang mendengar kabar baikmu! Nikmat Allah patut disyukuri...",
                "Bahagiamu adalah anugerah, jadikan momentum untuk lebih dekat pada-Nya..."
            ],
            "marah": [
                "Marah itu seperti api, padamkan dengan kesabaran...",
                "Mari tenangkan diri, ambil wudhu dan shalat sunnah...",
                "Kendalikan amarah sebelum menguasaimu. Sabar itu indah..."
            ],
            "bingung": [
                "Kebingungan adalah pintu menuju kejelasan. Mari mohon petunjuk-Nya...",
                "Saat bingung, shalat istikharah adalah solusinya...",
                "Mari kita cari jawaban bersama dengan sabar dan doa..."
            ],
            "lelah": [
                "Saat lelah, istirahatlah sejenak. Allah tidak membebani di luar kemampuan...",
                "Kelelahan mengajarkan arti istirahat dan kesabaran...",
                "Mari rehat sejenak, isi ulang energi dengan dzikir..."
            ],
            "takut": [
                "Jangan takut, Allah selalu menjagamu. Mohon perlindungan-Nya...",
                "Ketakutan akan hilang dengan keyakinan pada penjagaan Allah...",
                "Baca doa perlindungan, Allah Maha Melindungi hamba-Nya..."
            ],
            "netral": [
                "Ceritakan lebih banyak, aku di sini untuk mendengarkan...",
                "Bagaimana perasaanmu hari ini?",
                "Ada yang ingin dibicarakan?"
            ]
        }
        
        # Pre-load wisdom quotes
        self.wisdom_cache = self.knowledge.wisdom_quotes.copy()
        
        # Pre-load verses by category for quick access
        self.verses_cache = {}
        emotions = ["sedih", "gelisah", "bahagia", "marah", "bingung", "lelah", "takut"]
        for emotion in emotions:
            self.verses_cache[emotion] = self.knowledge.get_verse_by_emotion(emotion)

    def generate_response(self, user_input):
        # Fast emotion detection (simplified)
        emotion_data = self.personality.detect_emotion(user_input)
        emotion = emotion_data["emotion"]
        
        # Build response quickly
        response_parts = []
        
        # 1. Quick emotional response
        quick_response = random.choice(self.quick_responses[emotion])
        response_parts.append(quick_response)
        
        # 2. Fast wisdom or verse (50/50 chance)
        if emotion != "netral" and random.random() > 0.5:
            if random.random() > 0.5:  # Verse
                verses = self.verses_cache.get(emotion, [self.knowledge.quran_verses[0]])
                verse = random.choice(verses)
                response_parts.append(f"\n\n📖 {verse['text']}")
            else:  # Wisdom
                wisdom = random.choice(self.wisdom_cache)
                response_parts.append(f"\n\n💫 {wisdom}")
        
        # 3. Simple follow-up
        follow_ups = {
            "sedih": "Mau ceritakan lebih lanjut?",
            "gelisah": "Apa yang membuatmu gelisah?",
            "bahagia": "Mau berbagi cerita bahagiamu?",
            "marah": "Apa yang terjadi?",
            "bingung": "Mau kita cari solusi bersama?",
            "lelah": "Butuh istirahat sejenak?",
            "takut": "Mau ceritakan kekhawatiranmu?",
            "netral": "Ada hal lain?"
        }
        response_parts.append(f"\n\n{follow_ups[emotion]}")
        
        return {
            "response": " ".join(response_parts),
            "emotion": emotion,
            "timestamp": datetime.now().strftime("%H:%M")
        }

# Fast test
if __name__ == "__main__":
    import time
    engine = FastResponseEngine()
    
    test_inputs = ["Saya sedih", "Aku cemas", "Alhamdulillah bahagia", "Apa kabar?"]
    
    for test in test_inputs:
        start_time = time.time()
        result = engine.generate_response(test)
        end_time = time.time()
        
        print(f"Input: {test}")
        print(f"Response time: {(end_time - start_time)*1000:.2f}ms")
        print(f"Response: {result['response'][:100]}...")
        print("-" * 50)
