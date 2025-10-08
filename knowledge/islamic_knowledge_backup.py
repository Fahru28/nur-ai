# knowledge/islamic_knowledge.py
class IslamicKnowledge:
    def __init__(self):
        self.quran_verses = [
            {
                "ayat": "QS Al-Baqarah: 186",
                "text": "Dan apabila hamba-hamba-Ku bertanya kepadamu tentang Aku, maka sesungguhnya Aku dekat. Aku kabulkan permohonan orang yang berdoa apabila ia berdoa kepada-Ku.",
                "kategori": "doa, kedekatan Allah"
            },
            {
                "ayat": "QS Ar-Ra'd: 28",
                "text": "Orang-orang yang beriman dan hati mereka menjadi tenteram dengan mengingat Allah. Ingatlah, hanya dengan mengingat Allah hati menjadi tenteram.",
                "kategori": "ketenangan, dzikir"
            },
            {
                "ayat": "QS Al-Insyirah: 5-6", 
                "text": "Maka sesungguhnya bersama kesulitan ada kemudahan, sesungguhnya bersama kesulitan ada kemudahan.",
                "kategori": "kesulitan, harapan"
            },
            {
                "ayat": "QS Az-Zumar: 53",
                "text": "Katakanlah: 'Wahai hamba-hamba-Ku yang melampaui batas terhadap diri mereka sendiri! Janganlah kamu berputus asa dari rahmat Allah. Sesungguhnya Allah mengampuni dosa-dosa semuanya.'",
                "kategori": "ampunan, harapan"
            }
        ]
        
        self.hadith_list = [
            {
                "teks": "Sesungguhnya Allah itu indah dan menyukai keindahan.",
                "sumber": "HR Muslim",
                "kategori": "keindahan, akhlak"
            },
            {
                "teks": "Orang yang beriman itu mencintai saudaranya sebagaimana ia mencintai dirinya sendiri.",
                "sumber": "HR Bukhari",
                "kategori": "persaudaraan, cinta"
            }
        ]
        
        self.wisdom_quotes = [
            "Hati yang tenang adalah taman yang subur untuk iman tumbuh.",
            "Kesabaran itu seperti pohon, akarnya pahit tapi buahnya manis.",
            "Bersyukurlah dalam segala keadaan, karena setiap napas adalah anugerah.",
            "Kadang Allah memberi kita ujian bukan untuk menghukum, tapi untuk mengangkat derajat kita."
        ]
    
    def get_verse_by_emotion(self, emotion):
        verse_categories = {
            "sedih": ["harapan", "ampunan"],
            "gelisah": ["ketenangan", "dzikir"], 
            "bahagia": ["syukur", "nikmat"],
            "marah": ["sabar", "ampunan"],
            "bingung": "petunjuk"
        }
        
        target_categories = verse_categories.get(emotion, [])
        suitable_verses = []
        
        for verse in self.quran_verses:
            if any(cat in verse["kategori"] for cat in target_categories):
                suitable_verses.append(verse)
        
        return suitable_verses if suitable_verses else [self.quran_verses[0]]
    
    def get_wisdom(self):
        import random
        return random.choice(self.wisdom_quotes)
