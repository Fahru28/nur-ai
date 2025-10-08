from flask import Flask, request, jsonify
import random
import os

app = Flask(__name__)

# PRE-LOAD DATA - SUPER FAST ACCESS
QUOTES = [
    "Hati yang tenang adalah taman yang subur untuk iman tumbuh. 🌿",
    "Kesabaran itu seperti pohon, akarnya pahit tapi buahnya manis. 🌳",
    "Bersyukurlah dalam segala keadaan, karena setiap napas adalah anugerah. 🙏",
    "Ketika doa-doa tertunda, percayalah bahwa Allah sedang menyiapkan yang terbaik. 💫",
    "Dunia ini hanya jembatan, maka seberangilah dan jangan menjadikannya tempat tinggal. 🌉",
    "Ketenangan hati tidak diukur dari banyaknya harta, tapi dari cukupnya rasa syukur. 💖",
    "Masalah datang bukan untuk menjatuhkanmu, tapi untuk mengajarimu cara bangkit. 🚀",
    "Allah tidak pernah terlambat, Dia selalu tepat waktu dengan rencana terbaik-Nya. ⏰",
    "Jadikan Al-Quran sebagai sahabat, maka hidupmu akan penuh cahaya. 📖",
    "Kebahagiaan sejati adalah ketika hatimu tenang meski dunia sedang bergejolak. 🌙"
]

AYAT_QURAN = [
    "QS Al-Baqarah: 186 - 'Dan apabila hamba-hamba-Ku bertanya kepadamu tentang Aku, maka sesungguhnya Aku dekat. Aku kabulkan permohonan orang yang berdoa apabila ia berdoa kepada-Ku.'",
    "QS Ar-Ra'd: 28 - 'Orang-orang yang beriman dan hati mereka menjadi tenteram dengan mengingat Allah. Ingatlah, hanya dengan mengingat Allah hati menjadi tenteram.'",
    "QS Al-Insyirah: 5-6 - 'Maka sesungguhnya bersama kesulitan ada kemudahan, sesungguhnya bersama kesulitan ada kemudahan.'",
    "QS Az-Zumar: 53 - 'Katakanlah: Wahai hamba-hamba-Ku yang melampaui batas terhadap diri mereka sendiri! Janganlah kamu berputus asa dari rahmat Allah. Sesungguhnya Allah mengampuni dosa-dosa semuanya.'"
]

GREETINGS = [
    "Assalamu'alaikum warahmatullahi wabarakatuh! 🌙 Senang berbicara denganmu!",
    "Wa'alaikumussalam! Ada cerita atau perasaan apa yang ingin dibagi hari ini? 💭",
    "Alhamdulillah, senang mendengar darimu! Apa kabar hari ini? 🌟",
    "Salam sejahtera untukmu! Ceritakan apa yang ada di hati... ❤️",
    "Hai! Semoga harimu penuh berkah, ketenangan, dan cahaya ilahi! 💫"
]

# SUPER FAST RESPONSE ENGINE
def get_instant_response(user_input):
    user_input = user_input.lower().strip()
    
    # ULTRA-FAST KEYWORD MATCHING
    if any(word in user_input for word in ['quote', 'kutipan', 'motivasi', 'inspirasi', 'kata bijak']):
        return f"💫 {random.choice(QUOTES)}\n\nMau quotes lainnya atau ada cerita hari ini?", "inspirational"
    
    elif any(word in user_input for word in ['ayat', 'quran', 'al-quran', 'firman']):
        return f"📖 {random.choice(AYAT_QURAN)}\n\nMau ayat dengan tema tertentu?", "spiritual"
    
    elif any(word in user_input for word in ['hai', 'halo', 'hello', 'assalamu', 'selamat']):
        return f"{random.choice(GREETINGS)}", "welcoming"
    
    elif any(word in user_input for word in ['sedih', 'kecewa', 'menangis', 'putus asa', 'patah hati']):
        return "Wahai saudaraku, janganlah bersedih terlalu dalam... 💔\nAllah dekat dengan orang yang patah hati. Setiap kesedian membawa hikmah, percayalah pada rencana-Nya yang indah.", "sedih"
    
    elif any(word in user_input for word in ['cemas', 'khawatir', 'gelisah', 'takut', 'was-was']):
        return "Tenanglah wahai saudaraku... 🌿\nHanya dengan mengingat Allah hati menjadi tenteram. Mari tarik napas dalam dan serahkan semua pada Yang Maha Mengatur.", "gelisah"
    
    elif any(word in user_input for word in ['senang', 'bahagia', 'alhamdulillah', 'gembira']):
        return "Alhamdulillah! Senang mendengar kabar baikmu! 🎉\nSyukuri kebahagiaan ini dengan berbagi kebaikan pada sesama.", "bahagia"
    
    elif any(word in user_input for word in ['bingung', 'ragu', 'apa ya', 'gimana', 'tidak tahu']):
        return "Wah, sepertinya ada yang membuatmu bingung... 🤔\nMari kita cari kejelasan bersama. Kadang jawaban datang ketika kita sabar menunggu.", "bingung"
    
    elif any(word in user_input for word in ['marah', 'kesal', 'jengkel', 'dendam']):
        return "Marah itu seperti api, padamkan dengan kesabaran sebelum membakar... 🔥\nMari tenangkan hati, ambil wudhu dan ingatlah bahwa sabar itu indah.", "marah"
    
    elif any(word in user_input for word in ['lelah', 'capek', 'penat', 'letih']):
        return "Saat lelah, istirahatlah sejenak... 😴\nAllah tidak membebani di luar kemampuan. Tubuh butuh istirahat agar bisa beribadah lebih baik.", "lelah"
    
    else:
        responses = [
            "Ceritakan lebih banyak, aku sungguh-sungguh mendengarkan dengan sepenuh hati... 👂",
            "Apa yang ingin kamu bicarakan hari ini? Setiap cerita punya arti... 🌟",
            "Aku di sini untukmu, ceritakan apa yang ada di hati tanpa ragu... 💖",
            "Bagaimana perasaanmu saat ini? Kadang dengan bercerita, hati menjadi lebih ringan... 🌈"
        ]
        response = random.choice(responses)
        
        # 40% chance untuk tambah quote
        if random.random() < 0.4:
            quote = random.choice(QUOTES)
            response += f"\n\n💫 {quote}"
        
        return response, "netral"

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Nur AI - Teman Spiritual Online</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }
            .container {
                max-width: 400px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #2c7744 0%, #4a9c64 100%);
                color: white;
                padding: 25px;
                text-align: center;
            }
            .chat-container {
                height: 500px;
                overflow-y: auto;
                padding: 20px;
                background: #f8f9fa;
            }
            .message {
                margin: 10px 0;
                padding: 12px 16px;
                border-radius: 18px;
                max-width: 80%;
            }
            .user-message {
                background: #667eea;
                color: white;
                margin-left: auto;
                border-bottom-right-radius: 5px;
            }
            .ai-message {
                background: white;
                border: 1px solid #e0e0e0;
                border-bottom-left-radius: 5px;
            }
            .input-container {
                display: flex;
                padding: 15px;
                background: white;
                border-top: 1px solid #e0e0e0;
            }
            input {
                flex: 1;
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 25px;
                margin-right: 10px;
            }
            button {
                background: #2c7744;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 25px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>🌙 Nur AI Online</h2>
                <p>Teman Spiritual Anda - Now on Vercel!</p>
            </div>
            <div class="chat-container" id="chatContainer">
                <div class="message ai-message">
                    Assalamu'alaikum! 🌙<br><br>
                    Selamat datang di <strong>Nur AI Online</strong>!<br>
                    Saya sekarang berjalan di Vercel dengan kecepatan super!<br><br>
                    Ada yang bisa saya bantu hari ini?
                </div>
            </div>
            <div class="input-container">
                <input type="text" id="userInput" placeholder="Tulis pesan Anda..." autocomplete="off">
                <button onclick="sendMessage()">Kirim</button>
            </div>
        </div>

        <script>
            function sendMessage() {
                const input = document.getElementById('userInput');
                const message = input.value.trim();
                
                if (message) {
                    // Add user message
                    addMessage(message, 'user');
                    input.value = '';
                    
                    // Send to API
                    fetch('/api/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: message})
                    })
                    .then(response => response.json())
                    .then(data => {
                        addMessage(data.response, 'ai');
                    });
                }
            }
            
            function addMessage(text, sender) {
                const container = document.getElementById('chatContainer');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}-message`;
                messageDiv.textContent = text;
                container.appendChild(messageDiv);
                container.scrollTop = container.scrollHeight;
            }
            
            // Enter key support
            document.getElementById('userInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') sendMessage();
            });
        </script>
    </body>
    </html>
    '''

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                "response": "Maaf, pesan tidak boleh kosong...",
                "emotion": "netral"
            })
        
        response, emotion = get_instant_response(user_message)
        
        return jsonify({
            "response": response,
            "emotion": emotion
        })
        
    except Exception as e:
        return jsonify({
            "response": "Maaf, terjadi kesalahan. Silakan coba lagi...",
            "emotion": "netral"
        })

# Vercel compatible - no need to run if __main__
