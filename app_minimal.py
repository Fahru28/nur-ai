from flask import Flask, request, jsonify, render_template
import random
from datetime import datetime

app = Flask(__name__)

# Super fast responses - no AI processing
quick_responses = {
    "default": [
        "Assalamu'alaikum! Ada yang bisa Nur bantu? 🌙",
        "Ceritakan perasaanmu, aku di sini untuk mendengarkan...",
        "Mari kita bicara, apa yang ada di hatimu?",
        "Allah selalu mendengar setiap keluhan hamba-Nya...",
        "Setiap kesulitan pasti ada kemudahan, percayalah...",
        "Ketenangan datang dari mengingat Yang Maha Tenang...",
    ],
    "sad": [
        "Jangan bersedih, Allah dekat dengan orang yang patah hati...",
        "Setiap air mata akan diganti dengan senyuman...",
        "QS Az-Zumar: 53 - Janganlah berputus asa dari rahmat Allah...",
    ],
    "happy": [
        "Alhamdulillah! Syukuri kebahagiaan ini...",
        "Senang mendengar kabar baikmu!",
        "Bahagiamu adalah anugerah dari-Nya...",
    ]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower().strip()
    
    # Super fast emotion detection
    if any(word in user_message for word in ['sedih', 'kecewa', 'menangis']):
        category = "sad"
    elif any(word in user_message for word in ['senang', 'bahagia', 'alhamdulillah']):
        category = "happy" 
    else:
        category = "default"
    
    response = random.choice(quick_responses[category])
    
    return jsonify({
        "response": response,
        "emotion": category,
        "timestamp": datetime.now().strftime("%H:%M")
    })

if __name__ == '__main__':
    print("🌙 Nur AI SUPER FAST Starting...")
    print("📱 Access at: http://localhost:5000")
    print("⚡ Lightning speed!")
    app.run(host='0.0.0.0', port=5000, debug=False)
