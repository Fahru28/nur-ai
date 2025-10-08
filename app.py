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

# Enhanced rule-based responses (FALLBACK - JAUH LEBIH BAIK)
ENHANCED_RESPONSES = {
    "greeting": [
        "Assalamu'alaikum warahmatullahi wabarakatuh! 🌙 Senang sekali berbicara denganmu! Semoga Allah memberkahi percakapan kita...",
        "Wa'alaikumussalam! Cahaya pagi/sore/malam ini terasa lebih indah dengan kehadiranmu. Mari kita isi dengan percakapan yang penuh hikmah...",
        "Alhamdulillah, senang mendengar sapaan hangat darimu! Ada cerita atau perasaan apa yang ingin dibagi hari ini?",
    ],
    "sad": [
        "Wahai saudaraku, aku turut merasakan beratnya perasaanmu... 💔 Tapi ingatlah firman Allah: 'Sesungguhnya bersama kesulitan ada kemudahan' (QS Al-Insyirah: 6). Setiap air mata akan diganti dengan senyuman...",
        "Dengan penuh kasih sayang, aku mendengarmu... Kesedihanmu adalah ujian untuk menguatkan iman. Rasulullah bersabda: 'Sungguh menakjubkan urusan orang beriman, semua urusannya adalah baik baginya'...",
        "Mari kita hadapi ini bersama dengan sabar dan shalat... Allah tidak akan membebani hamba-Nya melampaui kemampuannya. Percayalah, setelah malam yang gelap pasti datang fajar...",
    ],
    "happy": [
        "Alhamdulillah! Senang sekali hatiku mendengar kabar baikmu! 🎉 Syukuri nikmat ini dengan meningkatkan ibadah dan berbagi pada sesama...",
        "Subhanallah! Kebahagiaanmu adalah bukti kasih sayang-Nya. Ingat firman Allah: 'Jika kamu bersyukur, niscaya Aku akan tambahkan nikmat-Ku kepadamu' (QS Ibrahim: 7)...",
        "Maha Suci Allah yang telah memberimu kebahagiaan! 💫 Jadikan momen ini untuk lebih mendekat pada-Nya dan berbuat kebaikan...",
    ],
    "confused": [
        "Wah, sepertinya ada yang membuatmu bingung... 🤔 Mari kita mohon petunjuk Allah dengan shalat istikharah. Kadang jawaban datang ketika kita sabar menunggu...",
        "Kebingungan adalah bagian dari proses belajar... Nabi Muhammad bersabda: 'Carilah ilmu sejak dari buaian hingga ke liang lahat'. Mari kita cari kejelasan bersama...",
        "Setiap kebingungan ada hikmahnya... Allah berfirman: 'Dan bertawakallah kepada Allah, cukuplah Allah sebagai pemelihara' (QS Al-Ahzab: 3). Mari kita serahkan pada-Nya...",
    ],
    "anxious": [
        "Tenanglah wahai saudaraku... 🌿 Ingatlah, hanya dengan mengingat Allah hati menjadi tenteram (QS Ar-Ra'd: 28). Mari kita perbanyak dzikir...",
        "Mari tarik napas dalam-dalam dan ucapkan: 'Hasbunallah wa ni'mal wakil' (Cukuplah Allah menjadi penolong kami)... Kegelisahan akan berlalu dengan izin-Nya...",
        "Setiap kegelisahan ada obatnya... Rasulullah mengajarkan: 'Ya Allah, sesungguhnya aku berlindung kepada-Mu dari keresahan dan kesedihan' (HR Bukhari). Mari kita amalkan...",
    ],
    "general": [
        "Ceritakan lebih banyak, aku sungguh-sungguh mendengarkan dengan sepenuh hati... 👂 Setiap cerita punya hikmahnya sendiri...",
        "Apa yang ingin kamu bicarakan hari ini? 🌟 Kadang dengan berbagi, beban hati menjadi lebih ringan...",
        "Aku di sini untukmu, ceritakan apa yang ada di hati... 💖 Dalam Islam, saling berbagi dan mendengarkan adalah ibadah...",
    ]
}

def detect_emotion(text):
    """Enhanced emotion detection"""
    text = text.lower()
    
    emotion_scores = {
        "sad": len([w for w in ['sedih', 'kecewa', 'menangis', 'putus asa', 'patah hati', 'sakit hati'] if w in text]),
        "happy": len([w for w in ['senang', 'bahagia', 'alhamdulillah', 'gembira', 'syukur', 'senang sekali'] if w in text]),
        "confused": len([w for w in ['bingung', 'ragu', 'tidak tahu', 'gimana', 'bagaimana', 'pusing'] if w in text]),
        "anxious": len([w for w in ['cemas', 'khawatir', 'takut', 'gelisah', 'was-was', 'deg-degan'] if w in text]),
        "greeting": len([w for w in ['hai', 'halo', 'assalamu', 'selamat', 'hai nur', 'hai nur ai'] if w in text])
    }
    
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    return dominant_emotion if emotion_scores[dominant_emotion] > 0 else "general"

def get_enhanced_response(emotion, user_input):
    """Get enhanced rule-based response"""
    response = random.choice(ENHANCED_RESPONSES.get(emotion, ENHANCED_RESPONSES["general"]))
    return response

def generate_gemini_response(user_input):
    """Generate response using Gemini with STRICT Islamic personality"""
    if not GEMINI_ACTIVE:
        emotion = detect_emotion(user_input)
        return get_enhanced_response(emotion, user_input)
    
    try:
        # STRICT Islamic personality prompt dengan contoh
        prompt = f"""
        ANDA ADALAH NUR AI - Asisten Spiritual Islami

        PERSONALITY KETAT:
        - AWALI dengan salam Islami: "Assalamu'alaikum" atau "Wa'alaikumussalam"
        - PANGGIL user dengan: "Wahai saudaraku" atau "Saudaraku"
        - BAHASA: Lembut, santun, penuh kasih sayang
        - SELIPKAN ayat Quran/hadits yang relevan
        - AKHIRI dengan doa atau harapan baik
        - GUNAKAN emoji Islami: 🌙, 💫, 🙏, 🌿
        - RESPONS: 2-3 paragraf saja

        CONTOH RESPONS YANG DIINGINKAN:
        User: "Hai"
        Nur AI: "Assalamu'alaikum warahmatullahi wabarakatuh! 🌙 Senang sekali mendengar sapaan darimu. Semoga Allah memberkahi hari dan percakapan kita dengan ketenangan dan hikmah..."

        User: "Aku sedih hari ini"  
        Nur AI: "Wahai saudaraku, aku turut merasakan kesedihanmu... 💔 Tapi ingatlah firman Allah: 'Janganlah kamu berputus asa dari rahmat Allah' (QS Az-Zumar: 53). Setiap kesedian adalah pembersih hati yang akan membuatmu lebih kuat. Mari kita hadapi ini dengan sabar dan shalat..."

        User: "Alhamdulillah dapat kabar baik"
        Nur AI: "Alhamdulillah! 💫 Senang mendengar kabar baikmu! Ingatlah untuk bersyukur, karena Allah berfirman: 'Jika kamu bersyukur, niscaya Aku akan tambahkan nikmat-Ku kepadamu'. Teruslah berbagi kebahagiaan dengan sesama..."

        SEKARANG USER BERKATA: "{user_input}"

        Responslah dengan STRICT mengikuti personality dan contoh di atas!
        """
        
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text
        else:
            emotion = detect_emotion(user_input)
            return get_enhanced_response(emotion, user_input)
            
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
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
        
        # Generate response
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
        "service": "Nur AI with Gemini",
        "gemini_active": GEMINI_ACTIVE,
        "mode": "islamic_personality_strict"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🌙 Nur AI - Strict Islamic Personality!")
    print("📱 Access at: http://localhost:5000")
    print(f"🧠 Gemini: {'ACTIVE ✅' if GEMINI_ACTIVE else 'FALLBACK MODE ⚠️'}")
    print("🎭 Personality: Lembut, Islami, Konsisten")
    app.run(host='0.0.0.0', port=port, debug=False)
