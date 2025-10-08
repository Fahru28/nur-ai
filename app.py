import os
import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

app = Flask(__name__)

print("🚀 Starting Nur AI - Deployed Version...")

# ===== SIMPLE AI LEARNING =====
class SimpleLearner:
    def __init__(self):
        self.knowledge_file = "islamic_knowledge.json"
        self.setup_initial_knowledge()
    
    def setup_initial_knowledge(self):
        initial_knowledge = {
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
        
        try:
            with open(self.knowledge_file, 'w', encoding='utf-8') as f:
                json.dump(initial_knowledge, f, ensure_ascii=False, indent=2)
            print("✅ Initial knowledge setup completed!")
        except Exception as e:
            print(f"❌ Knowledge setup error: {e}")

# ===== INITIALIZE =====
ai_learner = SimpleLearner()

# ===== KNOWLEDGE BASE =====
def load_knowledge():
    try:
        with open('islamic_knowledge.json', 'r', encoding='utf-8') as f:
            knowledge = json.load(f)
            total = sum(len(v) for v in knowledge.values())
            print(f"📚 Knowledge base loaded: {total} wisdom")
            return knowledge
    except Exception as e:
        print(f"❌ Error loading knowledge: {e}")
        return {
            "sabar": ["Sabar itu cahaya - HR Muslim"],
            "syukur": ["Bersyukurlah kepada Allah - QS Ibrahim: 7"],
            "shalat": ["Shalat adalah tiang agama"],
            "tasawuf": ["Tasawuf adalah membersihkan hati"],
            "akhlak": ["Sebaik-baik manusia adalah yang paling baik akhlaknya"]
        }

# ===== STATUS ENDPOINT =====
@app.route('/api/status')
def learning_status():
    knowledge = load_knowledge()
    total_wisdom = sum(len(wisdom_list) for wisdom_list in knowledge.values())
    
    return jsonify({
        "status": "Nur AI Deployed on Vercel",
        "total_knowledge": total_wisdom,
        "categories": {cat: len(wisdom) for cat, wisdom in knowledge.items()},
        "deployment": "Vercel + GitHub",
        "last_update": datetime.now().strftime("%H:%M:%S")
    })

# ===== CHAT INTERFACE =====
@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Nur AI - Deployed Version</title>
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
            .status-bar {
                background: #e8f5e8;
                padding: 12px 20px;
                border-bottom: 1px solid #c8e6c9;
                text-align: center;
                font-size: 0.9em;
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
            input[type="text"]:focus {
                border-color: #667eea;
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
            button:hover {
                opacity: 0.9;
            }
            .typing {
                color: #666;
                font-style: italic;
                padding: 12px 20px;
            }
            .deploy-badge {
                background: #000;
                color: white;
                padding: 3px 10px;
                border-radius: 12px;
                font-size: 0.7em;
                margin-left: 8px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌙 Nur AI 
                    <span class="deploy-badge">VERCEL</span>
                </h1>
                <p>Deployed Version - ChatGPT-like Islami</p>
            </div>
            
            <div class="status-bar">
                <strong>🚀 Status:</strong> 
                <span id="learningStatus">Deployed on Vercel</span>
                • <strong>📚 Knowledge:</strong> 
                <span id="knowledgeCount">Loading...</span>
            </div>
            
            <div class="chat-container" id="chatContainer">
                <div class="message ai-message">
                    <strong>Assalamu'alaikum! 🌟</strong><br>
                    Saya Nur AI versi deployed! Siap membantu dengan pengetahuan Islami.
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
                    chatContainer.removeChild(typingDiv);
                    addMessage(data.response);
                } catch (error) {
                    chatContainer.removeChild(typingDiv);
                    addMessage('❌ Maaf, terjadi kesalahan. Silakan coba lagi.');
                }
            }

            // Update status
            async function updateLearningStatus() {
                try {
                    const response = await fetch('/api/status');
                    const data = await response.json();
                    document.getElementById('knowledgeCount').textContent = data.total_knowledge;
                } catch (error) {
                    console.log('Gagal update status');
                }
            }

            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            updateLearningStatus();
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

        knowledge = load_knowledge()
        user_lower = user_message.lower()
        
        if any(greet in user_lower for greet in ['halo', 'hai', 'assalamu', 'hello']):
            response = "Wa'alaikumussalam! Ada yang bisa saya bantu? 🌙"
        
        elif 'sabar' in user_lower and knowledge['sabar']:
            import random
            response = random.choice(knowledge['sabar'])
            
        elif 'syukur' in user_lower and knowledge['syukur']:
            import random
            response = random.choice(knowledge['syukur'])
            
        elif 'shalat' in user_lower and knowledge['shalat']:
            import random
            response = random.choice(knowledge['shalat'])
            
        elif any(word in user_lower for word in ['tasawuf', 'sufi', 'zikir']) and knowledge['tasawuf']:
            import random
            response = random.choice(knowledge['tasawuf'])
            
        elif any(word in user_lower for word in ['akhlak', 'moral', 'etika']) and knowledge['akhlak']:
            import random
            response = random.choice(knowledge['akhlak'])
            
        elif any(word in user_lower for word in ['makasih', 'terima kasih']):
            response = "Sama-sama! Semoga bermanfaat. 😊"
            
        elif 'nama' in user_lower:
            response = "Saya Nur AI - Deployed on Vercel! 🚀"
            
        elif 'deploy' in user_lower or 'vercel' in user_lower:
            response = "Ya! Saya sudah di-deploy di Vercel dan GitHub. Bisa diakses dari mana saja! 🌍"
            
        else:
            if knowledge['sabar']:  # Fallback to sabar knowledge
                import random
                response = random.choice(knowledge['sabar'])
            else:
                response = "Pertanyaan bagus! Saya sedang terus dikembangkan. 😊"

        return jsonify({
            "response": response,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
    except Exception as e:
        return jsonify({"response": f"Maaf terjadi error: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Server running on: http://localhost:{port}")
    print("📚 Knowledge base: Ready")
    print("🌍 Deployment: Vercel Ready")
    print("⏹️  Press Ctrl+C to stop")
    app.run(host='0.0.0.0', port=port, debug=False)
