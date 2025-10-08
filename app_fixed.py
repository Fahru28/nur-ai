from flask import Flask, request, jsonify, render_template
import requests
import os
import random
from datetime import datetime

app = Flask(__name__)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBSPTuqaE2x1TP15lznwhCtSuZ4DfrFEWM')

def gemini_http_request(prompt):
    """Pakai Gemini via HTTP API dengan URL yang benar"""
    # URL YANG BENAR
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        print(f"🔄 Mengirim ke Gemini: {prompt[:50]}...")
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"❌ Gemini error: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Request error: {str(e)}")
        return None

# Fallback responses
RESPONSES = {
    "greeting": "Assalamu'alaikum! Senang berbicara denganmu! 🌙",
    "sad": "Wahai saudaraku, jangan bersedih... Allah dekat dengan orang yang patah hati. 💔",
    "happy": "Alhamdulillah! Senang mendengar kabar baikmu! 🎉",
}

def detect_emotion(text):
    text = text.lower()
    if 'sedih' in text: return "sad"
    elif 'senang' in text or 'alhamdulillah' in text: return "happy"
    elif 'hai' in text or 'halo' in text: return "greeting"
    else: return "general"

def generate_response(user_input):
    # Coba Gemini dulu
    prompt = f"""
    Anda adalah Nur AI - asisten spiritual Islami.
    Personality: Lembut, Islami, awali dengan salam.
    Respons 1-2 kalimat untuk: "{user_input}"
    """
    
    gemini_response = gemini_http_request(prompt)
    
    if gemini_response and len(gemini_response) > 5:
        print(f"✅ Gemini response: {gemini_response[:100]}...")
        return gemini_response
    else:
        # Fallback
        emotion = detect_emotion(user_input)
        fallback = RESPONSES.get(emotion, "Aku di sini untukmu...")
        print(f"🔄 Fallback: {fallback}")
        return fallback

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({"response": "Assalamu'alaikum! Pesan tidak boleh kosong. 🌙"})
        
        ai_response = generate_response(user_message)
        
        return jsonify({
            "response": ai_response,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
    except Exception as e:
        return jsonify({"response": "Assalamu'alaikum! Maaf terjadi kesalahan. 🌙"})

if __name__ == '__main__':
    print("🌙 Nur AI - Fixed Gemini URL")
    app.run(host='0.0.0.0', port=5000, debug=False)
