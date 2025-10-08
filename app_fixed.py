import os  # <--- INI YANG DITAMBAHIN
from flask import Flask, request, jsonify, render_template
import json
from datetime import datetime

app = Flask(__name__)

# ===== AUTO-LEARNING FEATURE =====
try:
    from islamic_learner import IslamicAILearner
    learner = IslamicAILearner()
    AUTO_LEARN_ENABLED = True
except:
    AUTO_LEARN_ENABLED = False
    print("⚠️  Auto-learning disabled (islamic_learner not found)")

# Knowledge base sederhana
ISLAMIC_KNOWLEDGE = {
    "sabar": [
        "Sabar itu cahaya - HR Muslim",
        "Allah menyukai orang-orang yang sabar - QS Ali Imran: 146"
    ],
    "syukur": [
        "Bersyukurlah kepada Allah - QS Ibrahim: 7",
        "Sesungguhnya jika kamu bersyukur, pasti Kami akan menambah nikmat kepadamu"
    ]
}

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Nur AI - ChatGPT-like</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
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
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .header { 
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 30px 20px;
                text-align: center;
            }
            .header h1 { 
                font-size: 2.5em; 
                margin-bottom: 10px;
                font-weight: 300;
            }
            .header p { 
                opacity: 0.9;
                font-size: 1.1em;
            }
            .chat-container { 
                height: 500px; 
                overflow-y: auto;
                padding: 20px;
                background: #f8f9fa;
            }
            .message { 
                margin: 15px 0;
                padding: 15px 20px;
                border-radius: 20px;
                max-width: 80%;
                line-height: 1.4;
                animation: fadeIn 0.3s ease-in;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
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
                gap: 10px;
            }
            input[type="text"] { 
                flex: 1; 
                padding: 15px 20px;
                border: 2px solid #e1e5e9;
                border-radius: 25px;
                font-size: 16px;
                outline: none;
                transition: all 0.3s ease;
            }
            input[type="text"]:focus {
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            button { 
                padding: 15px 25px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            .typing { 
                color: #666; 
                font-style: italic; 
                padding: 10px 20px;
            }
            .learn-feature {
                background: #e8f4fd;
                border: 1px solid #b6e0fe;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌙 Nur AI</h1>
                <p>AI Assistant Islami dengan Fitur Auto-Learning</p>
            </div>
            
            <div class="chat-container" id="chatContainer">
                <div class="message ai-message">
                    <strong>Assalamu'alaikum! 🌟</strong><br>
                    Saya Nur AI, siap membantu Anda. Saya juga bisa belajar otomatis dari website Islami!
                </div>
                ''' + ('''
                <div class="learn-feature">
                    <strong>🚀 Fitur Auto-Learning Aktif!</strong><br>
                    Kirim URL website Islami (seperti islam.nu.or.id) dan saya akan belajar otomatis!
                </div>
                ''' if AUTO_LEARN_ENABLED else '''
                <div class="learn-feature" style="background:#ffe6e6; border-color:#ffb3b3;">
                    <strong>⚠️ Fitur Auto-Learning Dimatikan</strong><br>
                    Module islamic_learner tidak ditemukan
                </div>
                ''') + '''
            </div>
            
            <div class="input-container">
                <input type="text" id="messageInput" placeholder="Ketik pesan atau URL website Islami..." autocomplete="off">
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

                // Add user message
                addMessage(message, true);
                messageInput.value = '';

                // Show typing indicator
                const typingDiv = document.createElement('div');
                typingDiv.className = 'typing';
                typingDiv.textContent = 'Nur AI sedang mengetik...';
                chatContainer.appendChild(typingDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;

                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: message })
                    });

                    const data = await response.json();
                    
                    // Remove typing indicator
                    chatContainer.removeChild(typingDiv);
                    
                    // Add AI response
                    addMessage(data.response);
                } catch (error) {
                    chatContainer.removeChild(typingDiv);
                    addMessage('❌ Maaf, terjadi kesalahan. Silakan coba lagi.');
                }
            }

            // Enter key support
            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            // Auto-focus input
            messageInput.focus();
        </script>
    </body>
    </html>
    '''

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({"response": "Assalamu'alaikum! Silakan ketik pesan."})

        # Auto-learning feature untuk URL
        if AUTO_LEARN_ENABLED and user_message.startswith(('http://', 'https://')):
            result = learner.safe_learn(user_message)
            if "error" in result:
                response = result["error"]
            else:
                response = f"🎉 {result['success']} Sekarang saya lebih pintar!"
        
        # Normal chat responses
        else:
            user_lower = user_message.lower()
            
            if 'sabar' in user_lower:
                response = ISLAMIC_KNOWLEDGE['sabar'][0]
            elif 'syukur' in user_lower:
                response = ISLAMIC_KNOWLEDGE['syukur'][0]
            elif any(word in user_lower for word in ['hai', 'halo', 'assalamu']):
                response = "Wa'alaikumussalam! Ada yang bisa saya bantu? 🌙"
            elif any(word in user_lower for word in ['makasih', 'terima kasih']):
                response = "Sama-sama! Semoga bermanfaat. 😊"
            else:
                response = "Pertanyaan bagus! Saya masih belajar. Coba tanya tentang sabar atau syukur."

        return jsonify({
            "response": response,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
    except Exception as e:
        return jsonify({"response": f"Maaf terjadi error: {str(e)}"})

@app.route('/api/learn', methods=['POST'])
def learn_from_url():
    if not AUTO_LEARN_ENABLED:
        return jsonify({"error": "Fitur auto-learning dimatikan"})
    
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({"error": "URL required"})
    
    result = learner.safe_learn(url)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🌙 Nur AI - ChatGPT-like Running...")
    print(f"🚀 Auto-learning: {'AKTIF' if AUTO_LEARN_ENABLED else 'DIMATIKAN'}")
    print(f"📱 Access at: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
