from flask import Flask, request, jsonify, render_template
import requests
import random
from datetime import datetime

app = Flask(__name__)

# Hugging Face API (gratis, no key needed for some models)
HUGGING_FACE_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"

def huggingface_chat(user_input, conversation_history=""):
    """Pakai Hugging Face AI yang gratis"""
    prompt = f"""
    [ISLAMIC PERSONALITY: Nur AI - Lembut, bijaksana, Islami]
    [STYLE: Awali dengan salam, panggil 'saudaraku', beri perspektif Islami]
    
    Previous: {conversation_history}
    User: {user_input}
    Nur AI:"""
    
    try:
        response = requests.post(
            HUGGING_FACE_URL,
            headers={"Authorization": "Bearer hf_your_token_here"},  # Optional for public models
            json={"inputs": prompt, "parameters": {"max_length": 150}},
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                ai_text = result[0]['generated_text']
                # Extract only the Nur AI response part
                if "Nur AI:" in ai_text:
                    return ai_text.split("Nur AI:")[-1].strip()
                return ai_text
        return None
    except:
        return None

# ENHANCED RULE-BASED FALLBACK (LEBIH SMART)
ISLAMIC_RESPONSES = {
    "greeting": [
        "Assalamu'alaikum warahmatullahi wabarakatuh! 🌙 Alhamdulillah, senang sekali bisa berbicara denganmu! Semoga Allah memberkahi percakapan kita...",
        "Wa'alaikumussalam! Cahaya pagi/sore/malam ini terasa lebih indah dengan kehadiranmu. Mari kita isi percakapan ini dengan dzikir dan kebaikan...",
    ],
    "sad": [
        "Wahai saudaraku, aku turut merasakan kesedihanmu... 💔 Tapi ingatlah: 'Setelah kesulitan pasti ada kemudahan' (QS Al-Insyirah: 6). Mari kita hadapi dengan sabar...",
        "Dengan penuh kasih sayang, aku mendengarmu... Kesedihan adalah pembersih hati. Rasulullah bersabda: 'Tidaklah seorang muslim tertimpa kesedihan... melainkan Allah akan menghapus dosa-dosanya' (HR Bukhari)...",
    ],
    "happy": [
        "Alhamdulillah! Senang sekali hatiku mendengar kabar baikmu! 🎉 Syukuri nikmat ini dan berbagilah dengan sesama...",
        "Subhanallah! Kebahagiaanmu adalah anugerah-Nya. 💫 Ingatlah untuk bersyukur: 'Jika kamu bersyukur, niscaya Aku akan tambahkan nikmat-Ku' (QS Ibrahim: 7)...",
    ],
    "thanks": [
        "Wa'alaikumussalam! Jazakallahu khairan! 🌟 Semoga Allah membalas semua kebaikanmu dengan yang lebih baik...",
        "Alhamdulillah! Senang bisa membantu. Mari kita lanjutkan perjalanan spiritual ini bersama... 💫",
    ],
    "confused": [
        "Wah, sepertinya ada yang membuatmu bingung... 🤔 Mari kita mohon petunjuk Allah. Kadang jawaban datang ketika kita sabar...",
        "Kebingungan adalah pintu menuju pemahaman... Allah berfirman: 'Dan bertawakallah kepada Allah, cukuplah Allah sebagai pemelihara' (QS At-Talaq: 3)...",
    ],
    "general": [
        "Ceritakan lebih banyak, aku sungguh-sungguh mendengarkan... 👂 Setiap cerita punya hikmahnya sendiri...",
        "Apa yang ingin kamu bicarakan hari ini? 🌟 Kadang dengan berbagi, beban hati menjadi lebih ringan...",
        "Aku di sini untukmu, ceritakan apa yang ada di hati... 💖 Dalam Islam, saling berbagi adalah ibadah...",
    ]
}

def smart_intent_detection(text):
    text = text.lower()
    
    if any(w in text for w in ['hai', 'halo', 'assalamu', 'selamat']): return "greeting"
    elif any(w in text for w in ['sedih', 'kecewa', 'menangis']): return "sad"
    elif any(w in text for w in ['senang', 'bahagia', 'alhamdulillah']): return "happy"
    elif any(w in text for w in ['terima kasih', 'makasih', 'thanks']): return "thanks"
    elif any(w in text for w in ['bingung', 'ragu', 'tau gak', 'gimana']): return "confused"
    elif any(w in text for w in ['ya', 'ok', 'oke', 'iye']): return "general"
    else: return "general"

def generate_ai_response(user_input):
    # 1. Coba Hugging Face AI dulu
    ai_response = huggingface_chat(user_input)
    
    if ai_response and len(ai_response) > 10:
        # Tambahkan sentuhan Islami ke respons AI
        if not ai_response.startswith(('Assalamu', 'Wa\'alaikum')):
            ai_response = "Assalamu'alaikum! " + ai_response
        return ai_response
    else:
        # 2. Fallback ke enhanced rule-based
        intent = smart_intent_detection(user_input)
        return random.choice(ISLAMIC_RESPONSES[intent])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({"response": "Assalamu'alaikum! Pesan tidak boleh kosong. 🌙"})
        
        ai_response = generate_ai_response(user_message)
        
        return jsonify({
            "response": ai_response,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
    except Exception as e:
        return jsonify({"response": "Assalamu'alaikum! Maaf terjadi kesalahan. 🌙"})

if __name__ == '__main__':
    print("🌙 Nur AI - Hugging Face + Enhanced Islamic Responses")
    print("📱 Access at: http://localhost:5000")
    print("💫 Free AI + Smart Fallback!")
    app.run(host='0.0.0.0', port=5000, debug=False)
