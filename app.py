from flask import Flask, request, jsonify
import random
from datetime import datetime

app = Flask(__name__)

ISLAMIC_KNOWLEDGE = {
    "sabar": [
        "Sabar itu cahaya - HR Muslim",
        "Allah menyukai orang-orang yang sabar - QS Ali Imran: 146", 
        "Sabar memiliki tiga derajat: sabar dalam ketaatan, sabar dari maksiat, dan sabar atas takdir"
    ],
    "syukur": [
        "Bersyukurlah kepada Allah - QS Ibrahim: 7",
        "Sesungguhnya jika kamu bersyukur, pasti Kami akan menambah nikmat kepadamu",
        "Syukur adalah mengakui nikmat Allah dalam hati, mengucapkannya dengan lisan, dan mengamalkannya dengan anggota badan"
    ],
    "shalat": [
        "Shalat adalah tiang agama",
        "Shalat mencegah perbuatan keji dan mungkar", 
        "Shalat lima waktu menghapus dosa-dosa kecil"
    ],
    "tasawuf": [
        "Tasawuf adalah membersihkan hati dan mendekatkan diri kepada Allah",
        "Ilmu tasawuf mengajarkan akhlak mulia dan penyucian jiwa"
    ],
    "akhlak": [
        "Sebaik-baik manusia adalah yang paling baik akhlaknya - HR Bukhari",
        "Akhlak mulia adalah buah dari keimanan yang benar"
    ]
}

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Nur AI - Vercel</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            }
            .header {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 25px;
                text-align: center;
            }
            .header h1 {
                font-size: 2em;
                margin-bottom: 8px;
            }
            .chat-container {
                height: 450px;
                overflow-y: auto;
                padding: 20px;
                background: #f8f9fa;
            }
            .message {
                margin: 12px 0;
                padding: 15px 20px;
                border-radius: 20px;
                max-width: 80%;
                line-height: 1.4;
            }
            .user-message {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin-left: auto;
                border-bottom-right-radius: 5px;
            }
            .ai-message {
                background: white;
                color: #333;
                border: 1px solid #e1e5e9;
                border-bottom-left-radius: 5px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }
            .input-container {
                padding: 20px;
                background: white;
                border-top: 1px solid #e1e5e9;
                display: flex;
                gap: 12px;
            }
            input[type="text"] {
                flex: 1;
                padding: 15px 20px;
                border: 2px solid #e1e5e9;
                border-radius: 25px;
                font-size: 16px;
                outline: none;
            }
            button {
                padding: 15px 25px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌙 Nur AI - Vercel</h1>
                <p>ChatGPT-like Islami - Successfully Deployed! 🚀</p>
            </div>
            
            <div class="chat-container" id="chatContainer">
                <div class="message ai-message">
                    <strong>Assalamu'alaikum! 🌟</strong><br>
                    Saya Nur AI versi Vercel! Berhasil di-deploy tanpa error!
                </div>
            </div>
            
            <div class="input-container">
                <input type="text" id="messageInput" placeholder="Tanya tentang Islam..." autocomplete="off">
                <button onclick="sendMessage()">Kirim</button>
            </div>
        </div>

        <script>
            const chatContainer = document.getElementById('chatContainer');
            const messageInput = document.getElementById('messageInput');

            function addMessage(message, isUser = false) {
                const messageDiv = document.createElement('div');
                messageDiv.className = isUser ? 'message user-message' : 'message ai-message';
                messageDiv.innerHTML = message;
                chatContainer.appendChild(messageDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }

            async function sendMessage() {
                const message = messageInput.value.trim();
                if (!message) return;

                addMessage(message, true);
                messageInput.value = '';

                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: message })
                    });

                    const data = await response.json();
                    addMessage(data.response);
                } catch (error) {
                    addMessage('❌ Maaf, terjadi kesalahan. Silakan coba lagi.');
                }
            }

            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            messageInput.focus();
        </script>
    </body>
    </html>
    '''

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip().lower()
        
        if not user_message:
            return jsonify({"response": "Assalamu'alaikum! Silakan ketik pesan."})

        if any(greet in user_message for greet in ['halo', 'hai', 'assalamu', 'hello']):
            response = "Wa'alaikumussalam! Ada yang bisa saya bantu? 🌙"
        
        elif 'sabar' in user_message:
            response = random.choice(ISLAMIC_KNOWLEDGE['sabar'])
            
        elif 'syukur' in user_message:
            response = random.choice(ISLAMIC_KNOWLEDGE['syukur'])
            
        elif 'shalat' in user_message:
            response = random.choice(ISLAMIC_KNOWLEDGE['shalat'])
            
        elif any(word in user_message for word in ['tasawuf', 'sufi', 'zikir']):
            response = random.choice(ISLAMIC_KNOWLEDGE['tasawuf'])
            
        elif any(word in user_message for word in ['akhlak', 'moral', 'etika']):
            response = random.choice(ISLAMIC_KNOWLEDGE['akhlak'])
            
        elif any(word in user_message for word in ['makasih', 'terima kasih']):
            response = "Sama-sama! Semoga bermanfaat. 😊"
            
        elif 'nama' in user_message:
            response = "Saya Nur AI - Berhasil di Vercel! 🚀"
            
        else:
            response = random.choice(ISLAMIC_KNOWLEDGE['sabar'] + ISLAMIC_KNOWLEDGE['syukur'])

        return jsonify({
            "response": response,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
    except Exception as e:
        return jsonify({"response": "Maaf, terjadi kesalahan sistem."})

if __name__ == '__main__':
    app.run(debug=False)
