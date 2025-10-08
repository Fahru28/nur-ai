# response_engine.py
from personality import NurAIPersonality
from knowledge.islamic_knowledge import IslamicKnowledge
import random
from datetime import datetime

class ResponseEngine:
    def __init__(self):
        self.personality = NurAIPersonality()
        self.knowledge = IslamicKnowledge()
        self.conversation_memory = []
        
        self.emotional_responses = {
            "sedih": {
                "strong": [
                    "Wahai saudaraku, peluk erat dari Nur... Allah tidak akan membiarkanmu sendirian dalam kesedihan ini.",
                    "Dengan nama Allah yang Maha Pengasih lagi Maha Penyayang... Mari kita hadapi ini bersama dengan iman.",
                    "Kesedihan yang mendalam ini aku rasakan bersamamu. Ingat, setelah malam yang gelap pasti datang fajar."
                ],
                "medium": [
                    "Wahai saudaraku, janganlah bersedih terlalu dalam. Setiap air mata akan diganti dengan senyuman...",
                    "Perasaan sedihmu aku pahami. Mari kita ingat, Allah dekat dengan orang yang patah hati...",
                    "Kesedihan adalah ujian untuk menguatkan hatimu. Percayalah, ada hikmah di baliknya..."
                ],
                "weak": [
                    "Sedikit kesedihan itu wajar, itu tanda hatimu masih hidup dan berperasaan...",
                    "Mari kita lihat sisi positifnya, setiap kesedian membawa pelajaran berharga...",
                    "Jangan biarkan kesedihan kecil mengaburkan banyaknya nikmat lainnya..."
                ]
            },
            "gelisah": {
                "strong": [
                    "Tenanglah wahai saudaraku, mari tarik napas dalam-dalam... Allah bersamamu dalam setiap langkah.",
                    "Kegelisahan yang besar ini bisa kita hadapi dengan dzikir dan tawakal...",
                    "Mari kita serahkan semua kekhawatiran pada Allah, Dia yang Maha Mengatur segalanya..."
                ],
                "medium": [
                    "Tenangkan hati sejenak... Ingatlah, hanya dengan mengingat Allah hati menjadi tenteram.",
                    "Kegelisahan itu seperti awan, sebentar lagi akan berlalu dengan izin Allah...",
                    "Mari kita cari ketenangan dengan shalat dan memohon perlindungan-Nya..."
                ],
                "weak": [
                    "Sedikit kegelisahan adalah alarm alami untuk lebih mendekat pada-Nya...",
                    "Rasa was-was kecil bisa kita atasi dengan memperbanyak istighfar...",
                    "Jangan biarkan kegelisahan kecil mengganggu ketenangan hatimu..."
                ]
            },
            "bahagia": {
                "strong": [
                    "Alhamdulillah! Senang sekali mendengar kebahagiaanmu! Nikmat Allah mana lagi yang kau dustakan?",
                    "Subhanallah! Bahagiamu adalah cahaya yang menerangi sekitarmu. Syukuri dengan berbagi!",
                    "Maha Suci Allah yang telah memberimu kebahagiaan! Jadikan momentum ini untuk lebih bersyukur..."
                ],
                "medium": [
                    "Alhamdulillah! Senang mendengar kabar baikmu. Teruslah bersyukur atas nikmat-Nya...",
                    "Bahagia itu anugerah, syukuri dengan meningkatkan ibadah dan kebaikan...",
                    "Kebahagiaanmu mengingatkanku pada betapa baiknya Allah kepada hamba-Nya..."
                ],
                "weak": [
                    "Alhamdulillah untuk perasaan baikmu hari ini...",
                    "Senang mendengarnya! Pertahankan energi positif ini...",
                    "Kebahagiaan kecil hari ini adalah nikmat yang patut disyukuri..."
                ]
            },
            "marah": {
                "strong": [
                    "Marah yang besar bisa membutakan hati. Mari ambil wudhu dan shalat dua rakaat...",
                    "Kemarahan adalah bara api, padamkan dengan kesabaran sebelum membakar...",
                    "Dengan nama Allah... Mari tenangkan diri sejenak. Kemarahan hanya akan merugikan diri sendiri."
                ],
                "medium": [
                    "Marah itu wajar, tapi kendalikan sebelum mengendalikanmu...",
                    "Mari tarik napas dalam, ucapkan 'A'udzubillah'... Kemarahan akan mereda dengan istighfar.",
                    "Jangan biarkan amarah menguasaimu. Ingat sabda Nabi: 'Orang kuat bukanlah yang bisa mengalahkan musuh, tapi yang bisa mengendalikan dirinya saat marah'."
                ],
                "weak": [
                    "Sedikit rasa kesal adalah ujian kesabaran...",
                    "Marah kecil mengajarkan kita untuk lebih sabar...",
                    "Jangan biarkan kesal sedikit merusak harimu..."
                ]
            },
            "bingung": {
                "strong": [
                    "Kebingungan yang mendalam adalah pintu menuju petunjuk Allah. Mari kita mohon hidayah-Nya...",
                    "Saat sangat bingung, shalat istikharah adalah jawabannya. Mintalah petunjuk pada Yang Maha Tahu...",
                    "Kebingungan besar ini akan berlalu dengan tawakal dan doa. Allah Maha Mengetahui yang terbaik."
                ],
                "medium": [
                    "Kebingungan adalah kesempatan untuk lebih mendekat pada Allah dalam pencarian jawaban...",
                    "Mari kita cari kejelasan bersama dengan sabar dan doa...",
                    "Setiap kebingungan ada hikmahnya, kadang kita perlu diam sejenak untuk menemukan arah..."
                ],
                "weak": [
                    "Sedikit kebingungan itu normal dalam perjalanan hidup...",
                    "Kebingungan kecil akan terpecahkan dengan ketenangan...",
                    "Jangan terburu-buru, jawaban akan datang dengan sendirinya..."
                ]
            },
            "lelah": {
                "strong": [
                    "Saat sangat lelah, ingatlah bahwa Allah tidak membebani di luar kemampuan. Istirahatlah sejenak...",
                    "Kelelahan yang mendalam adalah tanda untuk berhenti sejenak dan mengisi ulang energi spiritual...",
                    "Mari kita rehat sejenak, baca Al-Quran atau dzikir untuk mengembalikan ketenangan..."
                ],
                "medium": [
                    "Rasa lelah mengingatkan kita untuk lebih seimbang antara usaha dan istirahat...",
                    "Setiap keletihan ada pahalanya jika disertai niat yang ikhlas...",
                    "Mari ambil waktu untuk rileks sejenak, tubuh butuh istirahat agar bisa beribadah lebih baik..."
                ],
                "weak": [
                    "Sedikit kelelahan adalah bagian dari perjuangan...",
                    "Lelah kecil akan hilang dengan istirahat yang cukup...",
                    "Jangan lupa beri waktu untuk dirimu sendiri..."
                ]
            },
            "takut": {
                "strong": [
                    "Ketakutan yang besar hanya pada Allah yang pantas. Mari baca doa perlindungan...",
                    "Saat sangat takut, ingatlah bahwa Allah Maha Melindungi. Bacalah 'Hasbunallah wa ni'mal wakil'...",
                    "Takut yang mendalam akan hilang dengan memperbanyak dzikir dan tawakal pada Allah..."
                ],
                "medium": [
                    "Rasa takut adalah alarm alami untuk lebih mendekat pada Pelindung sejati...",
                    "Mari hadapi ketakutan dengan keyakinan bahwa Allah selalu menjaga...",
                    "Setiap rasa takut bisa diatasi dengan iman dan doa..."
                ],
                "weak": [
                    "Sedikit rasa takut adalah bentuk kewaspadaan...",
                    "Takut kecil mengingatkan kita untuk selalu memohon perlindungan-Nya...",
                    "Jangan biarkan kekhawatiran kecil mengganggumu..."
                ]
            },
            "netral": [
                "Ceritakan lebih banyak, aku di sini untuk mendengarkan...",
                "Bagaimana perasaanmu hari ini?",
                "Ada yang ingin kamu bicarakan? Aku siap mendengarkan...",
                "Hari ini bagaimana? Ada cerita apa?",
                "Aku di sini untukmu, ceritakan apa yang ada di hati..."
            ]
        }
    
    def generate_response(self, user_input):
        # Deteksi emosi dengan detail
        emotion_data = self.personality.detect_emotion(user_input)
        emotion = emotion_data["emotion"]
        intensity = emotion_data["intensity"]
        
        # Simpan ke memory
        self.conversation_memory.append({
            "input": user_input,
            "emotion": emotion,
            "timestamp": datetime.now().strftime("%H:%M"),
            "intensity": intensity
        })
        
        # Bangun response bertahap
        response_parts = []
        
        # 1. Emotional validation berdasarkan intensity
        if emotion != "netral":
            emotional_response = random.choice(self.emotional_responses[emotion][intensity])
            response_parts.append(emotional_response)
        else:
            emotional_response = random.choice(self.emotional_responses["netral"])
            response_parts.append(emotional_response)
        
        # 2. Wisdom atau ayat sesuai emosi dan intensity
        if emotion != "netral":
            # Untuk emotion strong, prioritaskan ayat Quran
            if intensity == "strong" or random.random() > 0.3:
                verses = self.knowledge.get_verse_by_emotion(emotion)
                if verses:
                    verse = random.choice(verses)
                    response_parts.append(f"\n\n📖 {verse['text']}\n— {verse['ayat']}")
            else:
                wisdom = self.knowledge.get_wisdom()
                response_parts.append(f"\n\n💫 {wisdom}")
        
        # 3. Practical advice berdasarkan emotion
        practical_advice = self._get_practical_advice(emotion, intensity)
        if practical_advice:
            response_parts.append(f"\n\n🛠️ {practical_advice}")
        
        # 4. Pertanyaan follow-up
        follow_up = self._get_follow_up_question(emotion, intensity)
        response_parts.append(f"\n\n{follow_up}")
        
        return {
            "response": " ".join(response_parts),
            "emotion": emotion,
            "intensity": intensity,
            "timestamp": self._get_timestamp()
        }
    
    def _get_practical_advice(self, emotion, intensity):
        advice_map = {
            "sedih": {
                "strong": "Cobalah shalat tahajud dan curahkan isi hatimu pada Allah dalam sujud yang panjang.",
                "medium": "Ambil wudhu, shalat dua rakaat, dan perbanyak istighfar.",
                "weak": "Baca Al-Quran sejenak atau dengarkan murotal yang menenangkan."
            },
            "gelisah": {
                "strong": "Lakukan shalat hajat dan perbanyak baca 'La hawla wa la quwwata illa billah'.",
                "medium": "Ambil napas dalam, dzikir 'Ya Hayyu Ya Qayyum' berulang kali.",
                "weak": "Sedekah kecil bisa menghilangkan kegelisahan, insyaAllah."
            },
            "marah": {
                "strong": "Segera ambil wudhu dan ubah posisi (dari berdiri jadi duduk, dari duduk jadi berbaring).",
                "medium": "Baca 'A'udzubillahi minasy syaithanir rajim' dan minum air perlahan.",
                "weak": "Diam sejenak dan hitung sampai 10 dalam hati."
            },
            "bingung": {
                "strong": "Lakukan shalat istikharah dan minta petunjuk pada Yang Maha Tahu.",
                "medium": "Tuliskan pilihan-pilihanmu dan minta pendapat orang shaleh.",
                "weak": "Istirahat sejenak, kadang kejelasan datang setelah pikiran rileks."
            },
            "lelah": {
                "strong": "Istirahat yang cukup, baca doa sebelum tidur, dan bangun untuk tahajud.",
                "medium": "Pijat ringan, minum air hangat, dan baca Al-Quran dengan perlahan.",
                "weak": "Pergi jalan-jalan sebentar menghirup udara segar."
            },
            "takut": {
                "strong": "Baca Ayat Kursi dan doa perlindungan, lalu serahkan semua pada Allah.",
                "medium": "Perbanyak shalawat dan istighfar, mintalah perlindungan-Nya.",
                "weak": "Ingatkan diri bahwa Allah selalu menjagamu dalam setiap kondisi."
            }
        }
        
        if emotion in advice_map:
            return advice_map[emotion].get(intensity, "")
        return ""
    
    def _get_follow_up_question(self, emotion, intensity):
        questions = {
            "sedih": {
                "strong": "Mau ceritakan lebih lanjut? Aku di sini untuk mendengarkan...",
                "medium": "Apa ada yang bisa Nur bantu untuk meringankan bebanmu?",
                "weak": "Mau kita cari kegiatan yang bisa menyenangkan hatimu?"
            },
            "gelisah": {
                "strong": "Mau kita praktikkan teknik menenangkan diri bersama?",
                "medium": "Apa sumber kegelisahanmu? Mungkin kita bisa cari solusinya...",
                "weak": "Mau coba kita alihkan perhatian dengan cerita inspiratif?"
            },
            "bahagia": {
                "strong": "Mau berbagi cerita kebahagiaanmu? Aku senang mendengarnya!",
                "medium": "Apa yang membuatmu bahagia? Ceritakan lebih banyak...",
                "weak": "Bagaimana cara mempertahankan energi positif ini?"
            },
            "marah": {
                "strong": "Apa yang bisa kita lakukan untuk meredakan ini bersama?",
                "medium": "Mau ceritakan apa yang terjadi? Mungkin dengan bercerita akan lebih lega...",
                "weak": "Mau kita cari cara untuk menyikapi situasi ini dengan lebih sabar?"
            },
            "bingung": {
                "strong": "Mau kita cari solusi bersama-sama?",
                "medium": "Apa yang membuatmu bingung? Mari kita analisis pelan-pelan...",
                "weak": "Mau diskusikan pilihan-pilihan yang ada?"
            },
            "lelah": {
                "strong": "Mau istirahat sejenak? Aku akan menunggu di sini...",
                "medium": "Apa yang membuatmu lelah? Mungkin kita bisa cari cara untuk meringankannya...",
                "weak": "Mau cari aktivitas yang lebih ringan dan menyenangkan?"
            },
            "takut": {
                "strong": "Mau kita baca doa perlindungan bersama?",
                "medium": "Apa yang membuatmu takut? Mari kita hadapi bersama...",
                "weak": "Mau ceritakan kekhawatiranmu? Kadang dengan bercerita rasa takut akan berkurang..."
            },
            "netral": "Ada hal lain yang ingin dibicarakan?"
        }
        
        if emotion in questions:
            if emotion == "netral":
                return questions[emotion]
            return questions[emotion].get(intensity, questions[emotion]["medium"])
        
        return "Ada yang ingin kamu tambahkan?"
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M")
    
    def get_conversation_summary(self):
        if len(self.conversation_memory) == 0:
            return "Belum ada percakapan"
        
        emotions = [entry["emotion"] for entry in self.conversation_memory[-5:]]  # last 5 entries
        emotion_count = {}
        for emotion in emotions:
            emotion_count[emotion] = emotion_count.get(emotion, 0) + 1
        
        dominant_emotion = max(emotion_count, key=emotion_count.get) if emotion_count else "netral"
        return f"Percakapan terakhir cenderung {dominant_emotion}"

# Test the enhanced engine
if __name__ == "__main__":
    engine = ResponseEngine()
    test_inputs = [
        "Saya sedih banget hari ini",
        "Aku cemas berat tentang masa depan",
        "Alhamdulillah dapat kabar baik banget",
        "Apa kabar?",
        "Aku marah besar sama dia",
        "Lelah banget hari ini",
        "Takut sekali dengan keputusan ini"
    ]
    
    for test in test_inputs:
        print(f"Input: {test}")
        result = engine.generate_response(test)
        print(f"Emotion: {result['emotion']} ({result['intensity']})")
        print(f"Response: {result['response']}")
        print("-" * 80)
