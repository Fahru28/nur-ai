from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini dengan API Key Anda
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    GEMINI_ACTIVE = True
else:
    GEMINI_ACTIVE = False
    print("⚠️  Gemini API Key not found, using fallback mode")

# Fallback responses untuk ketika Gemini tidak aktif
FALLBACK_RESPONSES = {
    "greeting": [
        "Assalamu'alaikum warahmatullahi wabarakatuh! 🌙 Senang berbicara denganmu!",
        "Wa'alaikumussalam! Semoga harimu penuh berkah dan ketenangan...",
        "Alhamdulillah, senang mendengar darimu! Ada yang bisa saya bantu?"
    ],
    "sad": [
        "Wahai saudaraku, janganlah bersedih... Allah dekat dengan orang yang patah hati. 💔",
        "Setiap kesedian membawa hikmah, percayalah pada rencana-Nya yang indah...",
        "Mari kita hadapi ini bersama dengan iman dan kesabaran..."
    ],
    "happy": [
        "Alhamdulillah! Senang mendengar kabar baikmu! 🎉",
        "Subhanallah! Bahagiamu adalah anugerah dari-Nya...",
        "Syukuri kebahagiaan ini dengan berbagi kebaikan pada sesama..."
    ],
    "confused": [
        "Wah, sepertinya ada yang membuatmu bingung... 🤔",
        "Mari kita cari kejelasan bersama...",
        "Kebingungan adalah pintu menuju pemahaman..."
    ],
    "general": [
        "Ceritakan lebih banyak, aku sungguh-sungguh mendengarkan...",
        "Apa yang ada di hati dan pikiranmu saat ini?",
        "Aku di sini untukmu, ceritakan apa yang ingin dibagi..."
    ]
}

def detect_emotion(text):
    """Simple emotion detection"""
    text = text.lower()
    if any(word in text for word in ['sedih', 'kecewa', 'menangis']):
        return "sad"
    elif any(word in text for word in ['senang', 'bahagia', 'alhamdulillah']):
        return "happy" 
    elif any(word in text for word in ['bingung', 'ragu', 'tidak tahu']):
        return "confused"
    elif any(word in text for word in ['hai', 'halo', 'assalamu']):
        return "greeting"
    else:
        return "general"

def get_fallback_response(emotion):
    """Get fallback response based on emotion"""
    import random
    return random.choice(FALLBACK_RESPONSES.get(emotion, FALLBACK_RESPONSES["general"]))

def generate_gemini_response(user_input):
    """Generate response menggunakan Gemini dengan personality Islami"""
    if not GEMINI_ACTIVE:
        return get_fallback_response(detect_emotion(user_input))
    
    try:
        # System prompt untuk personality Islami
        prompt = f"""
        Anda adalah Nur AI, asisten spiritual Islami yang lembut dan penuh hikmah.
        
        Personality:
        - Lembut, bijaksana, penuh kasih sayang
        - Menggunakan bahasa Indonesia yang santun
        - Selalu merespons dengan salam Islami
        - Memberikan perspektif Islami yang menenangkan
        - Mengutip ayat Quran/hadits ketika relevan
        
        Contoh:
        - "Assalamu'alaikum warahmatullahi wabarakatuh 🌙"
        - "Wahai saudaraku, ..."
        - "Alhamdulillah, ..."
        - "Mari kita renungkan bersama ..."
        
        User berkata: "{user_input}"
        
        Responslah sebagai Nur AI dengan personality di atas.
        Buat respons yang menenangkan, bermakna, dan tidak terlalu panjang.
        """
        
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text
        else:
            return get_fallback_response(detect_emotion(user_input))
            
    except Exception as e:
        print(f"Gemini Error: {e}")
        return get_fallback_response(detect_emotion(user_input))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                "response": "Assalamu'alaikum! Pesan tidak boleh kosong. 🌙",
                "emotion": "neutral",
                "timestamp": datetime.now().strftime("%H:%M")
            })
        
        # Generate response (Gemini atau fallback)
        ai_response = generate_gemini_response(user_message)
        emotion = detect_emotion(user_message)
        
        return jsonify({
            "response": ai_response,
            "emotion": emotion,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
    except Exception as e:
        return jsonify({
            "response": "Assalamu'alaikum! Maaf terjadi kesalahan. Mari kita coba lagi. 🌙",
            "emotion": "neutral", 
            "timestamp": datetime.now().strftime("%H:%M")
        })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "Nur AI with Gemini",
        "gemini_active": GEMINI_ACTIVE,
        "mode": "gemini_enhanced"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🌙 Nur AI Enhanced with Gemini!")
    print("📱 Access at: http://localhost:5000")
    print(f"🧠 Gemini: {'ACTIVE ✅' if GEMINI_ACTIVE else 'FALLBACK MODE ⚠️'}")
    app.run(host='0.0.0.0', port=port, debug=False)
