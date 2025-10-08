from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
import random
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_ACTIVE = False
model = None

if GEMINI_API_KEY and GEMINI_API_KEY != "your_actual_gemini_api_key_here":
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        GEMINI_ACTIVE = True
        print("✅ Gemini AI Activated!")
    except Exception as e:
        print(f"❌ Gemini configuration failed: {e}")
        GEMINI_ACTIVE = False
else:
    print("⚠️  Gemini API Key not found, using enhanced rule-based mode")

# IMPROVED RESPONSES - LEBIH SPESIFIK DAN BERMAKNA
ENHANCED_RESPONSES = {
    "greeting": [
        "Assalamu'alaikum warahmatullahi wabarakatuh! 🌙 Alhamdulillah, senang sekali bisa berbicara denganmu! Semoga Allah memberkahi percakapan kita dengan ketenangan dan hikmah yang bermanfaat...",
        "Wa'alaikumussalam! Cahaya pagi/sore/malam ini terasa lebih indah dengan kehadiranmu. Mari kita isi percakapan ini dengan dzikir dan kebaikan...",
        "Alhamdulillah, senang mendengar sapaan hangat darimu! Ada cerita, perasaan, atau pertanyaan apa yang ingin kita bahas bersama hari ini?",
    ],
    "sad": [
        "Wahai saudaraku, aku turut merasakan kesedihan yang kau alami... 💔 Tapi ingatlah firman Allah: 'Janganlah kamu berputus asa dari rahmat Allah. Sesungguhnya Allah mengampuni dosa-dosa semuanya.' (QS Az-Zumar: 53). Mari kita hadapi ini dengan sabar dan shalat, percayalah setiap kesedian akan diganti dengan kebahagiaan...",
        "Dengan penuh kasih sayang, aku mendengarmu... Kesedihanmu adalah ujian untuk menguatkan iman. Rasulullah bersabda: 'Sungguh menakjubkan urusan orang beriman, semua urusannya adalah baik baginya. Jika mendapat kesenangan ia bersyukur, dan itu baik baginya. Jika mendapat kesusahan ia bersabar, dan itu baik baginya.' (HR Muslim). Mari kita bersabar bersama...",
        "Mari kita hadapi kesedian ini dengan tawakal... Allah berfirman: 'Dan bersabarlah kamu, sesungguhnya Allah beserta orang-orang yang sabar.' (QS Al-Anfal: 46). Setiap air mata kesedihan akan menjadi pembersih hati, dan setelah kesulitan pasti datang kemudahan...",
    ],
    "happy": [
        "Alhamdulillah! Senang sekali hatiku mendengar kabar baikmu! 🎉 Ingatlah untuk bersyukur, karena Allah berfirman: 'Jika kamu bersyukur, niscaya Aku akan tambahkan nikmat-Ku kepadamu.' (QS Ibrahim: 7). Teruslah berbagi kebahagiaan dengan sesama, karena senyummu di depan saudaramu adalah sedekah...",
        "Subhanallah! Kebahagiaanmu adalah bukti kasih sayang-Nya yang tak terhingga. 💫 Rasulullah bersabda: 'Sebaik-baik manusia adalah yang paling bermanfaat bagi manusia.' Mari manfaatkan kebahagiaanmu untuk berbuat kebaikan pada sesama...",
        "Maha Suci Allah yang telah memberimu kebahagiaan! Syukuri nikmat ini dengan meningkatkan ibadah dan membantu mereka yang membutuhkan. Bahagiamu akan lebih berarti ketika bisa menjadi cahaya bagi orang lain...",
    ],
    "confused": [
        "Wah, sepertinya ada yang membuatmu bingung dan tidak tahu arah... 🤔 Mari kita mohon petunjuk Allah dengan shalat istikharah. Rasulullah bersabda: 'Jika salah seorang di antara kalian berkeinginan melakukan sesuatu, hendaklah ia shalat sunnah dua rakaat...' (HR Bukhari). Kadang jawaban terbaik datang ketika kita bersabar dan bertawakal...",
        "Kebingungan adalah bagian dari proses mencari makna... Allah berfirman: 'Dan barang siapa yang bertawakal kepada Allah, niscaya Allah akan mencukupkan keperluannya.' (QS At-Talaq: 3). Mari kita serahkan semua kebingungan pada Yang Maha Mengetahui yang terbaik...",
        "Setiap kebingungan membawa kita lebih dekat pada pencerahan... Nabi Muhammad mengajarkan: 'Mintalah fatwa kepada hatimu, kebaikan adalah apa yang menenangkan jiwa dan hati.' Mari kita dengarkan suara hati dengan tenang dan penuh keyakinan...",
    ],
    "question": [
        "Pertanyaan yang bagus! 🤔 Mari kita renungkan bersama... Dalam mencari jawaban, kita diajarkan untuk berdoa: 'Ya Allah, tunjukkanlah yang benar itu benar dan berilah kekuatan untuk mengikutinya, dan tunjukkanlah yang batil itu batil dan berilah kekuatan untuk menjauhinya.'",
        "Aku memahami keingintahuanmu... 🌟 Mari kita cari jawaban dengan sabar. Allah berfirman: 'Dan bertanyalah kepada orang yang mempunyai pengetahuan jika kamu tidak mengetahui.' (QS An-Nahl: 43). Setiap pertanyaan adalah pintu menuju pemahaman...",
        "Mari kita eksplorasi pertanyaanmu bersama... 💭 Dalam Islam, menuntut ilmu adalah ibadah. Rasulullah bersabda: 'Menuntut ilmu wajib bagi setiap muslim.' (HR Ibnu Majah). Semoga Allah membukakan pintu pemahaman untuk kita...",
    ],
    "general": [
        "Ceritakan lebih banyak, aku sungguh-sungguh mendengarkan dengan sepenuh hati... 👂 Setiap cerita punya hikmah dan pelajaran berharga. Mari kita ambil hikmah dari apa yang kau alami...",
        "Apa yang ingin kamu bicarakan hari ini? 🌟 Kadang dengan berbagi cerita, beban hati menjadi lebih ringan dan kita bisa saling menguatkan dalam kebaikan...",
        "Aku di sini untukmu, ceritakan apa yang ada di hati... 💖 Dalam Islam, saling berbagi dan mendengarkan adalah bentuk sedekah yang mulia. Semoga percakapan kita membawa ketenangan...",
    ]
}

# Quran verses untuk berbagai situasi
QURAN_VERSES = {
    "sad": [
        "QS Al-Insyirah: 5-6 - 'Maka sesungguhnya bersama kesulitan ada kemudahan, sesungguhnya bersama kesulitan ada kemudahan.'",
        "QS Al-Baqarah: 286 - 'Allah tidak membebani seseorang melainkan sesuai dengan kesanggupannya...'", 
        "QS Az-Zumar: 53 - 'Katakanlah: Wahai hamba-hamba-Ku yang melampaui batas terhadap diri mereka sendiri! Janganlah kamu berputus asa dari rahmat Allah...'"
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

def detect_emotion(text):
    """IMPROVED emotion detection dengan lebih banyak keyword"""
    text = text.lower()
    
    # Expanded keyword lists
    emotion_scores = {
        "sad": len([w for w in ['sedih', 'kecewa', 'menangis', 'putus asa', 'patah hati', 'sakit hati', 'galau', 'murung'] if w in text]),
        "happy": len([w for w in ['senang', 'bahagia', 'alhamdulillah', 'gembira', 'syukur', 'senang sekali', 'bahagia banget', 'asyik'] if w in text]),
        "confused": len([w for w in ['bingung', 'ragu', 'tidak tahu', 'gimana', 'bagaimana', 'pusing', 'dilema', 'tau gak', 'ngapain'] if w in text]),
        "anxious": len([w for w in ['cemas', 'khawatir', 'takut', 'gelisah', 'was-was', 'deg-degan', 'tidak tenang', 'gugup'] if w in text]),
        "greeting": len([w for w in ['hai', 'halo', 'assalamu', 'selamat', 'hai nur', 'hai nur ai', 'hello'] if w in text]),
        "question": len([w for w in ['?', 'apa', 'bagaimana', 'kenapa', 'mengapa', 'kapan', 'siapa', 'tau gak', 'tahu gak'] if w in text])
    }
    
    # Special case untuk "tau gak" dan typo "bingun"
    if "tau gak" in text or "tahu gak" in text:
        emotion_scores["question"] += 2
    if "bingun" in text:  # Handle typo
        emotion_scores["confused"] += 2
    
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    return dominant_emotion if emotion_scores[dominant_emotion] > 0 else "general"

def get_enhanced_response(emotion, user_input):
    """Get enhanced response dengan Quran verses"""
    response = random.choice(ENHANCED_RESPONSES.get(emotion, ENHANCED_RESPONSES["general"]))
    
    # Add Quran verse untuk emotional states (70% chance)
    if emotion in ["sad", "happy", "confused"] and random.random() < 0.7:
        verse = random.choice(QURAN_VERSES.get(emotion, QURAN_VERSES["sad"]))
        response += f"\n\n📖 {verse}"
    
    return response

def generate_gemini_response(user_input):
    """Generate response - NONAKTIFKAN GEMINI, PAKAI ENHANCED RULE-BASED"""
    # Untuk sementara NONAKTIFKAN Gemini, pakai rule-based yang sudah diperbaiki
    emotion = detect_emotion(user_input)
    return get_enhanced_response(emotion, user_input)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                "response": "Assalamu'alaikum! Pesan tidak boleh kosong. Ada yang bisa saya bantu? 🌙",
                "emotion": "neutral",
                "timestamp": datetime.now().strftime("%H:%M")
            })
        
        # Generate response (PAKAI RULE-BASED YANG SUDAH DIPERBAIKI)
        ai_response = generate_gemini_response(user_message)
        emotion = detect_emotion(user_message)
        
        return jsonify({
            "response": ai_response,
            "emotion": emotion,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "response": "Assalamu'alaikum! Maaf terjadi kesalahan. Mari kita coba lagi dengan percakapan yang penuh hikmah. 🌙",
            "emotion": "neutral", 
            "timestamp": datetime.now().strftime("%H:%M")
        })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "Nur AI - Enhanced Rule-Based",
        "mode": "improved_islamic_responses"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🌙 Nur AI - Enhanced Islamic Responses!")
    print("📱 Access at: http://localhost:5000")
    print("🎭 Mode: Improved Rule-Based (No Gemini)")
    print("📚 Features: Better emotion detection, Quran verses, meaningful responses")
    app.run(host='0.0.0.0', port=port, debug=False)
