# Temporary fix - kita update method _extract_topics

def _extract_topics_fixed(self, text):
    """Fixed topic extraction - less aggressive"""
    text = text.lower()
    topics = []
    
    # Hanya extract topic jika ada konteks yang jelas
    topic_keywords = {
        "keluarga": {
            "keywords": ["keluarga", "orang tua", "ibu", "ayah", "saudara", "adik", "kakak"],
            "min_words": 3  # Butuh minimal 3 kata dalam kalimat
        },
        "pekerjaan": {
            "keywords": ["kerja", "pekerjaan", "kantor", "bos", "rekan kerja", "gaji"],
            "min_words": 3
        },
        "studi": {
            "keywords": ["sekolah", "kuliah", "belajar", "ujian", "tugas", "guru", "dosen"],
            "min_words": 3  
        },
        "kesehatan": {
            "keywords": ["sakit", "sehat", "dokter", "rumah sakit", "obat", "periksa"],
            "min_words": 3
        },
        "spiritual": {
            "keywords": ["shalat", "doa", "quran", "islam", "iman", "allah", "masjid"],
            "min_words": 3
        }
    }
    
    word_count = len(text.split())
    
    for topic, config in topic_keywords.items():
        keywords = config["keywords"]
        min_words = config["min_words"]
        
        # Only extract topic if we have enough context
        if word_count >= min_words and any(keyword in text for keyword in keywords):
            topics.append(topic)
    
    return list(set(topics))

def _get_personal_touch_fixed(self):
    """Fixed personal touch - only after meaningful conversation"""
    if self.user_profile["conversation_count"] <= 2:  # Minimal 2x chat dulu
        return ""
    
    # Only use personal touch if we have recent meaningful topics
    recent_topics = list(set(self.user_profile["topics_discussed"][-3:]))
    
    if len(recent_topics) >= 1:  # Minimal ada 1 topic yang clear
        topic = recent_topics[0]
        personal_touches = {
            "keluarga": "Oh ya, tentang keluarga...",
            "pekerjaan": "Mengenai pekerjaan...", 
            "studi": "Tentang belajar...",
            "kesehatan": "Mengenai kesehatan...",
            "spiritual": "Tentang spiritual..."
        }
        return personal_touches.get(topic, "")
    
    return ""
