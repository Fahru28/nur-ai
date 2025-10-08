from flask import Flask, request, jsonify, render_template
import requests
import os
import random
from datetime import datetime

app = Flask(__name__)

# Ambil API Key dari environment variable Vercel
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBSPTuqaE2x1TP15lznwhCtSuZ4DfrFEWM')

def gemini_http_request(prompt):
    """Pakai Gemini via HTTP API"""
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return None
    except:
        return None

# Enhanced fallback responses
RESPONSES = {
    "greeting": [
        "Assalamu'alaikum warahmatullahi wabarakatuh! 🌙 Senang sekali berbicara denganmu! Semoga Allah memberkahi percakapan kita dengan ketenangan dan hikmah...",
        "Wa'alaikumussalam! Cahaya pagi/sore/malam ini terasa lebih indah dengan kehadiranmu. Mari kita isi percakapan ini dengan dzikir dan kebaikan...",
    ],
    "sad": [
        "Wahai saudaraku, aku turut merasakan kesedihanmu... 💔 Tapi ingatlah firman Allah: 'Janganlah kamu berputus asa dari rahmat Allah. Sesungguhnya Allah mengampuni dosa-dosa semuanya.' (QS Az-Zumar: 53)...",
        "Dengan penuh kasih sayang, aku mendengarmu... Kesedihanmu adalah ujian untuk menguatkan iman. Mari kita hadapi ini dengan sabar dan shalat...",
    ],
    "happy": [
        "Alhamdulillah! Senang sekali hatiku mendengar kabar baikmu! 🎉 Ingatlah untuk bersyukur, karena Allah berfirman: 'Jika kamu bersyukur, niscaya Aku akan tambahkan nikmat-Ku kepadamu.' (QS Ibrahim: 7)...",
        "Subhanallah! Kebahagiaanmu adalah bukti kasih sayang-Nya. 💫 Teruslah berbagi kebahagiaan dengan sesama...",
    ]
}

def detect_emotion(text):
    text = text.lower()
    if any(w in text for w in ['sedih', 'kecewa']): return "sad"
    elif any(w in text for w in ['senang', 'bahagia', 'alhamdulillah']): return "happy" 
    elif any(w in text for w in ['bingung', 'ragu']): return "confused"
    elif any(w in text for w in ['hai', 'halo', 'assalamu']): return "greeting"
    else: return "general"

def generate_response(user_input):
    # Coba pakai Gemini dulu
    prompt = f"""
    Anda adalah Nur AI - asisten spiritual Islami.
    
    Personality:
    - Lembut, bijaksana, penuh kasih sayang
    - Awali dengan salam Islami
    - Panggil user: "Wahai saudaraku" 
    - Berikan perspektif Islami
    - Respons 2-3 kalimat saja
    
    User: "{user_input}"
    
    Responslah dengan personality di atas.
    """
    
    gemini_response = gemini_http_request(prompt)
    
    if gemini_response and len(gemini_response) > 10:
        return gemini_response
    else:
        # Fallback ke rule-based
        emotion = detect_emotion(user_input)
        return random.choice(RESPONSES.get(emotion, ["Aku di sini untukmu..."]))

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
                "timestamp": datetime.now().strftime("%H:%M")
            })
        
        ai_response = generate_response(user_message)
        
        return jsonify({
            "response": ai_response,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
    except Exception as e:
        return jsonify({
            "response": "Assalamu'alaikum! Maaf terjadi kesalahan. 🌙",
            "timestamp": datetime.now().strftime("%H:%M")
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🌙 Nur AI - Vercel + Gemini HTTP API!")
    print("📱 Ready for deployment!")
    app.run(host='0.0.0.0', port=port, debug=False)
