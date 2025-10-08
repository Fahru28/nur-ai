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
            },
            {
                "ayat": "QS Al-Baqarah: 286",
                "text": "Allah tidak membebani seseorang melainkan sesuai dengan kesanggupannya...",
                "kategori": "kesabaran, kemampuan"
            },
            {
                "ayat": "QS At-Talaq: 3",
                "text": "Dan memberinya rezeki dari arah yang tiada disangka-sangkanya. Dan barangsiapa yang bertawakkal kepada Allah niscaya Allah akan mencukupkan keperluannya.",
                "kategori": "rezeki, tawakal"
            },
            {
                "ayat": "QS Al-Ankabut: 69",
                "text": "Dan orang-orang yang berjihad untuk (mencari keridhaan) Kami, benar-benar akan Kami tunjukkan kepada mereka jalan-jalan Kami.",
                "kategori": "usaha, petunjuk"
            },
            {
                "ayat": "QS Al-Hijr: 49",
                "text": "Kabarkanlah kepada hamba-hamba-Ku, bahwa sesungguhnya Aku Maha Pengampun lagi Maha Penyayang.",
                "kategori": "ampunan, kasih sayang"
            },
            {
                "ayat": "QS Al-An'am: 162",
                "text": "Katakanlah: sesungguhnya shalatku, ibadahku, hidupku dan matiku hanyalah untuk Allah, Tuhan semesta alam.",
                "kategori": "tujuan hidup, ibadah"
            },
            {
                "ayat": "QS Al-Mujadilah: 7",
                "text": "Dan tidak ada sesuatupun yang sama dengan-Nya, dan Dia-lah Yang Maha Mendengar lagi Maha Melihat.",
                "kategori": "tauhid, keyakinan"
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
            },
            {
                "teks": "Senyummu di depan saudaramu adalah sedekah.",
                "sumber": "HR Tirmidzi",
                "kategori": "senyum, sedekah"
            },
            {
                "teks": "Janganlah kamu saling membenci, saling mendengki, dan saling membelakangi. Jadilah kamu hamba-hamba Allah yang bersaudara.",
                "sumber": "HR Bukhari-Muslim",
                "kategori": "persaudaraan, perdamaian"
            },
            {
                "teks": "Barangsiapa beriman kepada Allah dan hari akhir, maka hendaklah ia berkata baik atau diam.",
                "sumber": "HR Bukhari-Muslim",
                "kategori": "bicara baik, akhlak"
            },
            {
                "teks": "Sesungguhnya Allah tidak melihat kepada rupa dan harta kalian, tetapi Dia melihat kepada hati dan amal kalian.",
                "sumber": "HR Muslim",
                "kategori": "hati, amal"
            },
            {
                "teks": "Tidak sempurna iman seseorang di antara kamu hingga ia mencintai untuk saudaranya apa yang ia cintai untuk dirinya sendiri.",
                "sumber": "HR Bukhari-Muslim",
                "kategori": "iman, cinta"
            },
            {
                "teks": "Sebaik-baik manusia adalah yang paling bermanfaat bagi manusia.",
                "sumber": "HR Thabrani",
                "kategori": "manfaat, akhlak"
            }
        ]
        
        self.wisdom_quotes = [
            "Hati yang tenang adalah taman yang subur untuk iman tumbuh.",
            "Kesabaran itu seperti pohon, akarnya pahit tapi buahnya manis.",
            "Bersyukurlah dalam segala keadaan, karena setiap napas adalah anugerah.",
            "Kadang Allah memberi kita ujian bukan untuk menghukum, tapi untuk mengangkat derajat kita.",
            "Dunia ini hanya jembatan, maka seberangilah jembatan itu dan jangan menjadikannya tempat tinggal.",
            "Ketenangan hati tidak diukur dari banyaknya harta, tapi dari cukupnya rasa syukur.",
            "Ketika doa-doa tertunda, percayalah bahwa Allah sedang menyiapkan yang terbaik.",
            "Jangan sedih jika impianmu tertunda, mungkin Allah ingin memberimu yang lebih baik.",
            "Kesulitan mengajarkan kita makna kesabaran, dan kesabaran membawa kita pada kemenangan.",
            "Setiap pagi adalah lembaran baru, tuliskan dengan kebaikan dan penuh harap pada-Nya.",
            "Allah tidak pernah terlambat, Dia selalu tepat waktu dengan rencana terbaik-Nya.",
            "Ketika kamu merasa sendirian, ingatlah bahwa Allah lebih dekat dari urat lehermu.",
            "Kebahagiaan sejati adalah ketika hatimu tenang meski dunia sedang bergejolak.",
            "Jadikan Al-Quran sebagai sahabat, maka hidupmu akan penuh cahaya.",
            "Masalah datang bukan untuk menjatuhkanmu, tapi untuk mengajarimu cara bangkit."
        ]
        
        self.daily_prayers = [
            "Ya Allah, berikan kami hati yang tenang dan pikiran yang jernih hari ini.",
            "Ya Rabb, mudahkanlah urusan kami dan lapangkanlah hati kami.",
            "Ya Allah, jadikan hari ini lebih baik dari kemarin dan esok lebih baik dari hari ini.",
            "Ya Tuhan kami, berilah kami kebaikan di dunia dan kebaikan di akhirat.",
            "Ya Allah, cukupkanlah kami dengan rezeki-Mu yang halal dan jauhkan dari yang haram.",
            "Ya Rahman, sembuhkanlah hati-hati yang terluka dan tenangkan jiwa-jiwa yang gelisah."
        ]
    
    def get_verse_by_emotion(self, emotion):
        verse_categories = {
            "sedih": ["harapan", "ampunan", "kesabaran"],
            "gelisah": ["ketenangan", "dzikir", "tawakal"], 
            "bahagia": ["syukur", "nikmat", "kebahagiaan"],
            "marah": ["sabar", "ampunan", "perdamaian"],
            "bingung": ["petunjuk", "usaha", "keyakinan"],
            "lelah": ["kesabaran", "kemampuan", "usaha"],
            "takut": ["perlindungan", "keyakinan", "tawakal"]
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
    
    def get_daily_prayer(self):
        import random
        return random.choice(self.daily_prayers)
    
    def get_hadith_by_topic(self, topic):
        suitable_hadith = []
        for hadith in self.hadith_list:
            if topic in hadith["kategori"]:
                suitable_hadith.append(hadith)
        return suitable_hadith if suitable_hadith else [self.hadith_list[0]]
