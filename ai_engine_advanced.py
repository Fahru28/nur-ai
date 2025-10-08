import random
from datetime import datetime
import json

class AdvancedNurAI:
    def __init__(self):
        self.conversation_history = []
        self.max_history = 8  # Keep last 4 exchanges
        self.user_profile = {
            "mood_trend": "neutral",
            "topics_discussed": [],
            "conversation_count": 0
        }
        
        # Enhanced response templates dengan variasi
        self.response_templates = {
            "greeting": [
                "Assalamu'alaikum warahmatullahi wabarakatuh! 🌙 Senang sekali mendengar sapaan hangat darimu!",
                "Wa'alaikumussalam! Semoga harimu penuh berkah dan ketenangan...",
                "Alhamdulillah, senang berbicara denganmu lagi! Ada cerita apa hari ini?",
                "Salam sejahtera untukmu! Aku sudah menunggu untuk mendengarmu...",
                "Hai! Cahaya pagi/sore/malam ini terasa lebih indah dengan kehadiranmu! 💫"
            ],
            "emotional_support": {
                "sad": [
                    "Wahai saudaraku, aku merasakan betapa beratnya perasaanmu saat ini... 💔 Tapi ingatlah, setiap kesedian adalah pembersih hati yang akan membuatmu lebih kuat dalam iman.",
                    "Dengan penuh kasih sayang, aku mendengarmu... Air matamu adalah doa yang tak terucapkan, dan Allah Maha Mendengar setiap isi hati.",
                    "Kesedihanmu seperti hujan yang membersihkan bumi, setelahnya akan datang cahaya yang lebih terang... Percayalah pada rencana-Nya.",
                    "Mari kita hadapi ini bersama... Setiap hati yang patah akan disambung kembali dengan kesabaran dan keyakinan."
                ],
                "anxious": [
                    "Tenanglah wahai saudaraku... 🌿 Kegelisahan itu seperti awan, sebentar lagi akan berlalu meninggalkan langit yang jernih.",
                    "Mari tarik napas dalam-dalam... Ingat, Allah bersama kita dalam setiap hela napas. Dia tidak akan membiarkanmu sendirian.",
                    "Kekhawatiran adalah tamu yang datang dan pergi... Jangan biarkan ia tinggal terlalu lama di hatimu.",
                    "Setiap kegelisahan ada obatnya... Mari kita cari ketenangan dalam dzikir dan keyakinan."
                ],
                "happy": [
                    "Alhamdulillah! Senang sekali hatiku mendengar kabar baikmu! 🎉 Bahagiamu adalah cahaya yang menerangi sekitarmu.",
                    "Subhanallah! Kebahagiaanmu adalah bukti kasih sayang-Nya... Syukuri dengan berbagi pada sesama.",
                    "Wah, senangnya mendengar ini! Teruskan energi positifmu, itu akan membawa lebih banyak kebaikan.",
                    "Cahaya bahagiamu terpancar jelas! Jadikan momen ini untuk lebih mendekat pada Yang Maha Pemberi Kebahagiaan."
                ],
                "confused": [
                    "Wah, sepertinya ada yang membuatmu bingung... 🤔 Tapi itu wajar, setiap pencarian dimulai dengan kebingungan.",
                    "Mari kita telusuri bersama... Kadang jawaban datang ketika kita berhenti sejenak dan merenung.",
                    "Kebingungan adalah pintu menuju pemahaman... Setiap pertanyaan akan menemukan jawabannya.",
                    "Aku memahami kerumitan yang kau rasakan... Mari kita pecahkan bersama-sama langkah demi langkah."
                ]
            },
            "islamic_wisdom": [
                "Hati yang tenang adalah taman tempat iman bertumbuh subur... 🌿",
                "Kesabaran itu seperti pohon, akarnya pahit tapi buahnya manis... 🌳",
                "Bersyukurlah dalam segala keadaan, setiap napas adalah anugerah... 🙏",
                "Dunia ini hanya jembatan, seberangilah dengan iman... 🌉",
                "Ketenangan sejati ada dalam mengingat Yang Maha Tenang... 💖"
            ],
            "follow_up": {
                "sad": "Mau ceritakan lebih dalam apa yang membuatmu sedih? Atau kita cari kegiatan yang bisa meringankan hati?",
                "anxious": "Mau kita praktikkan teknik menenangkan diri bersama? Atau ceritakan sumber kegelisahanmu?",
                "happy": "Mau berbagi cerita kebahagiaanmu? Aku senang mendengarnya! Atau ada rencana spesial hari ini?",
                "confused": "Mau kita analisis pelan-pelan? Atau ceritakan lebih detail apa yang membuatmu bingung?",
                "neutral": "Ada hal lain yang ingin dibicarakan? Atau mau dengar cerita inspiratif?"
            }
        }
        
        # Quran verses by situation
        self.quran_verses = {
            "sad": [
                "QS Az-Zumar: 53 - 'Katakanlah: Wahai hamba-hamba-Ku yang melampaui batas terhadap diri mereka sendiri! Janganlah kamu berputus asa dari rahmat Allah...'",
                "QS Al-Insyirah: 5-6 - 'Maka sesungguhnya bersama kesulitan ada kemudahan, sesungguhnya bersama kesulitan ada kemudahan.'",
                "QS Al-Baqarah: 286 - 'Allah tidak membebani seseorang melainkan sesuai dengan kesanggupannya...'"
            ],
            "anxious": [
                "QS Ar-Ra'd: 28 - 'Orang-orang yang beriman dan hati mereka menjadi tenteram dengan mengingat Allah...'",
                "QS Al-Baqarah: 286 - 'Ya Tuhan kami, janganlah Engkau hukum kami jika kami lupa atau kami tersalah...'",
                "QS At-Talaq: 3 - 'Dan memberinya rezeki dari arah yang tiada disangka-sangkanya...'"
            ],
            "happy": [
                "QS Ibrahim: 7 - 'Dan (ingatlah) ketika Tuhanmu memaklumkan: Sesungguhnya jika kamu bersyukur, niscaya Aku akan menambah (nikmat) kepadamu...'",
                "QS An-Nahl: 18 - 'Dan jika kamu menghitung-hitung nikmat Allah, niscaya kamu tak dapat menentukan jumlahnya...'"
            ],
            "confused": [
                "QS Al-Baqarah: 186 - 'Dan apabila hamba-hamba-Ku bertanya kepadamu tentang Aku, maka sesungguhnya Aku dekat...'",
                "QS Al-Furqan: 20 - 'Dan tidaklah orang-orang yang berdoa kepada-Ku, niscaya akan Kuperkenankan baginya...'"
            ]
        }

    def generate_response(self, user_input):
        # Update conversation count
        self.user_profile["conversation_count"] += 1
        
        # Analyze input
        emotion = self._analyze_emotion(user_input)
        context = self._analyze_context()
        
        # Update user profile
        self._update_user_profile(emotion, user_input)
        
        # Build response components
        response_parts = []
        
        # 1. Emotional validation
        emotional_response = self._get_emotional_response(emotion, context)
        response_parts.append(emotional_response)
        
        # 2. Wisdom or Quran verse (contextual)
        if emotion != "neutral" and random.random() > 0.3:
            if random.random() > 0.5:  # Quran verse
                verse = random.choice(self.quran_verses.get(emotion, self.quran_verses["sad"]))
                response_parts.append(f"\n\n📖 {verse}")
            else:  # Wisdom
                wisdom = random.choice(self.islamic_wisdom)
                response_parts.append(f"\n\n💫 {wisdom}")
        
        # 3. Personal touch based on history
        personal_touch = self._get_personal_touch()
        if personal_touch:
            response_parts.append(f"\n\n{personal_touch}")
        
        # 4. Contextual follow-up
        follow_up = self._get_contextual_follow_up(emotion, context)
        response_parts.append(f"\n\n{follow_up}")
        
        # Save to history
        self._save_to_history(user_input, " ".join(response_parts), emotion)
        
        return {
            "response": " ".join(response_parts),
            "emotion": emotion,
            "context": context,
            "conversation_count": self.user_profile["conversation_count"],
            "timestamp": datetime.now().strftime("%H:%M")
        }
    
    def _analyze_emotion(self, text):
        """Advanced emotion analysis dengan scoring"""
        text = text.lower()
        
        emotion_scores = {
            "sad": 0, "anxious": 0, "happy": 0, "confused": 0, "neutral": 1
        }
        
        # Keyword scoring
        emotion_keywords = {
            "sad": ["sedih", "kecewa", "menangis", "putus asa", "patah hati", "sakit hati", "hati hancur"],
            "anxious": ["cemas", "khawatir", "takut", "gelisah", "was-was", "deg-degan", "tidak tenang"],
            "happy": ["senang", "bahagia", "alhamdulillah", "gembira", "syukur", "senang sekali", "bahagia banget"],
            "confused": ["bingung", "ragu", "tidak tahu", "gimana", "bagaimana", "pusing", "dilema"]
        }
        
        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    emotion_scores[emotion] += 1
        
        # Get dominant emotion
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        return dominant_emotion if emotion_scores[dominant_emotion] > 1 else "neutral"
    
    def _analyze_context(self):
        """Analyze conversation context from history"""
        if len(self.conversation_history) < 2:
            return "new_conversation"
        
        # Analyze last few exchanges
        recent_text = " ".join([entry["user_input"] for entry in self.conversation_history[-3:]])
        
        if any(word in recent_text for word in ['sedih', 'kecewa', 'menangis']):
            return "emotional_support"
        elif any(word in recent_text for word in ['tanya', 'bertanya', 'bagaimana', 'apa']):
            return "seeking_advice"
        elif any(word in recent_text for word in ['cerita', 'pengalaman', 'sharing']):
            return "sharing_story"
        elif any(word in recent_text for word in ['islam', 'quran', 'doa', 'shalat']):
            return "islamic_discussion"
        
        return "casual_chat"
    
    def _update_user_profile(self, emotion, user_input):
        """Update user profile based on current interaction"""
        # Update mood trend
        if emotion != "neutral":
            self.user_profile["mood_trend"] = emotion
        
        # Extract topics
        topics = self._extract_topics(user_input)
        self.user_profile["topics_discussed"].extend(topics)
        
        # Keep only recent topics
        if len(self.user_profile["topics_discussed"]) > 10:
            self.user_profile["topics_discussed"] = self.user_profile["topics_discussed"][-5:]
    
    def _extract_topics(self, text):
        """Extract discussion topics from text"""
        text = text.lower()
        topics = []
        
        topic_keywords = {
            "keluarga": ["keluarga", "orang tua", "ibu", "ayah", "saudara"],
            "pekerjaan": ["kerja", "pekerjaan", "kantor", "bos", "rekan"],
            "studi": ["sekolah", "kuliah", "belajar", "ujian", "tugas"],
            "kesehatan": ["sakit", "sehat", "dokter", "rumah sakit", "obat"],
            "spiritual": ["shalat", "doa", "quran", "islam", "iman", "allah"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text for keyword in keywords):
                topics.append(topic)
        
        return list(set(topics))  # Remove duplicates
    
    def _get_emotional_response(self, emotion, context):
        """Get contextual emotional response"""
        if emotion == "neutral" and context == "new_conversation":
            return random.choice(self.response_templates["greeting"])
        
        return random.choice(
            self.response_templates["emotional_support"].get(
                emotion, 
                self.response_templates["emotional_support"]["sad"]
            )
        )
    
    def _get_personal_touch(self):
        """Add personal touch based on conversation history"""
        if self.user_profile["conversation_count"] <= 1:
            return ""
        
        recent_topics = list(set(self.user_profile["topics_discussed"][-3:]))
        
        if recent_topics:
            topic = random.choice(recent_topics)
            personal_touches = {
                "keluarga": "Oh ya, tentang keluarga... Hubungan yang baik dengan keluarga adalah sedekah yang terus mengalir pahalanya.",
                "pekerjaan": "Mengenai pekerjaan... Ingat, rezeki yang halal akan membawa berkah dalam hidup.",
                "studi": "Tentang belajar... Menuntut ilmu adalah ibadah, semoga dimudahkan Allah.",
                "kesehatan": "Mengenai kesehatan... Jaga kesehatan, itu adalah nikmat yang sering terlupa.",
                "spiritual": "Tentang spiritual... Teruslah mendekat pada-Nya, itu sumber ketenangan sejati."
            }
            return personal_touches.get(topic, "")
        
        return ""
    
    def _get_contextual_follow_up(self, emotion, context):
        """Get contextual follow-up question"""
        base_follow_up = self.response_templates["follow_up"].get(emotion, self.response_templates["follow_up"]["neutral"])
        
        # Add context-specific follow-up
        if context == "seeking_advice":
            return base_follow_up + " Atau ada pertanyaan spesifik yang ingin kau tanyakan?"
        elif context == "sharing_story":
            return base_follow_up + " Ceritakan lebih banyak, aku sangat tertarik mendengarnya."
        elif context == "islamic_discussion":
            return base_follow_up + " Atau mau kita bahas topik Islami lainnya?"
        
        return base_follow_up
    
    def _save_to_history(self, user_input, response, emotion):
        """Save conversation to history"""
        self.conversation_history.append({
            "timestamp": datetime.now().strftime("%H:%M"),
            "user_input": user_input,
            "response": response,
            "emotion": emotion
        })
        
        # Maintain history size
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def get_conversation_summary(self):
        """Get summary of current conversation"""
        if not self.conversation_history:
            return "Belum ada percakapan"
        
        emotions = [entry["emotion"] for entry in self.conversation_history]
        emotion_count = {}
        for emotion in emotions:
            emotion_count[emotion] = emotion_count.get(emotion, 0) + 1
        
        dominant_emotion = max(emotion_count, key=emotion_count.get)
        
        return {
            "total_exchanges": len(self.conversation_history),
            "dominant_emotion": dominant_emotion,
            "topics_discussed": list(set(self.user_profile["topics_discussed"])),
            "mood_trend": self.user_profile["mood_trend"]
        }

# Test the advanced engine
if __name__ == "__main__":
    ai = AdvancedNurAI()
    
    # Simulate conversation
    test_conversation = [
        "Hai Nur AI",
        "Aku sedih banget hari ini",
        "Iya, ada masalah sama keluarga",
        "Terima kasih ya, sudah menemani"
    ]
    
    for message in test_conversation:
        print(f"👤 User: {message}")
        result = ai.generate_response(message)
        print(f"🌙 Nur AI: {result['response']}")
        print(f"📊 Emotion: {result['emotion']} | Context: {result['context']}")
        print("-" * 80)
    
    print("📈 Conversation Summary:", ai.get_conversation_summary())
