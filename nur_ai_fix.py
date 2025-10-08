import os
import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import json
import re
import threading
from datetime import datetime

app = Flask(__name__)

print("🚀 Starting Nur AI - Auto Learning Background...")

# ===== BACKGROUND AUTO-LEARNING =====
class BackgroundLearner:
    def __init__(self):
        # PAKAI WEB YANG KAMU KASIH + tambahan
        self.learning_sources = [
            "https://nu.or.id/tasawuf-akhlak/ini-tiga-derajat-sabar-dalam-kajian-tasawuf-dqfyE",
            "https://nu.or.id/tasawuf-akhlak",
            "https://islam.nu.or.id/artikel"
        ]
        self.is_learning = False
        self.learned_count = 0
        
    def start_auto_learning(self):
        def learning_loop():
            self.is_learning = True
            try:
                print("🔄 AI sedang belajar otomatis di background...")
                for source in self.learning_sources:
                    learned = self.learn_from_source(source)
                    if learned:
                        print(f"📚 Berhasil belajar dari: {source[:50]}...")
                
                self.learned_count += 1
                print(f"✅ Round {self.learned_count} selesai! Total wisdom bertambah.")
                
                # Jadwal belajar lagi 5 menit kemudian
                print("⏰ Akan belajar lagi dalam 5 menit...")
                threading.Timer(300, learning_loop).start()
                
            except Exception as e:
                print(f"❌ Learning error: {e}")
                threading.Timer(300, learning_loop).start()
        
        learning_loop()
        print("🎯 Auto-learning started!")
    
    def learn_from_source(self, source_url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(source_url, timeout=10, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Untuk URL spesifik (yang kamu kasih)
            if "tiga-derajat-sabar" in source_url:
                return self.learn_from_specific_url(soup)
            
            # Untuk halaman list artikel
            article_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if any(keyword in href.lower() for keyword in ['artikel', 'tasawuf', 'sabar', 'syukur', 'akhlak']):
                    if href.startswith('http'):
                        article_links.append(href)
                    elif href.startswith('/'):
                        article_links.append("https://nu.or.id" + href)
            
            # Belajar dari 1 artikel pertama
            for article_url in article_links[:1]:
                if article_url.startswith('http'):
                    self.learn_from_article(article_url)
                    return True
                    
        except Exception as e:
            print(f"❌ Error learning from {source_url}: {e}")
        return False
    
    def learn_from_specific_url(self, soup):
        """Belajar dari URL spesifik yang kamu kasih"""
        try:
            islamic_wisdom = []
            
            # Extract konten utama
            content_selectors = ['article', '.post-content', '.entry-content', '.content', 'main']
            
            for selector in content_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text().strip()
                    if self.is_islamic_content(text):
                        # Bersihkan dan split paragraf
                        paragraphs = re.split(r'\n\s*\n', text)
                        for para in paragraphs:
                            para = para.strip()
                            if len(para) > 50 and self.is_islamic_content(para):
                                clean_para = self.clean_content(para)
                                if clean_para and clean_para not in islamic_wisdom:
                                    islamic_wisdom.append(clean_para)
                                    print(f"➕ Learned: {clean_para[:60]}...")
            
            if islamic_wisdom:
                self.save_wisdom(islamic_wisdom)
                return True
                
        except Exception as e:
            print(f"❌ Error learning specific: {e}")
        return False
    
    def learn_from_article(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, timeout=10, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            content_selectors = ['article', '.post-content', '.entry-content', '.content']
            islamic_wisdom = []
            
            for selector in content_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text().strip()
                    if self.is_islamic_content(text):
                        paragraphs = re.split(r'\n\s*\n', text)
                        for para in paragraphs[:3]:  # Ambil 3 paragraf pertama
                            para = para.strip()
                            if len(para) > 50 and self.is_islamic_content(para):
                                clean_para = self.clean_content(para)
                                if clean_para and clean_para not in islamic_wisdom:
                                    islamic_wisdom.append(clean_para)
            
            if islamic_wisdom:
                self.save_wisdom(islamic_wisdom)
                return True
            
        except Exception as e:
            print(f"❌ Error learning article: {e}")
        return False
    
    def is_islamic_content(self, text):
        islamic_keywords = [
            'allah', 'rasulullah', 'islam', 'muslim', 'quran', 'hadits', 
            'sabar', 'syukur', 'shalat', 'puasa', 'tasawuf', 'akhlak',
            'derajat', 'iman', 'taqwa', 'tawakal', 'ikhlas'
        ]
        text_lower = text.lower()
        return sum(1 for keyword in islamic_keywords if keyword in text_lower) >= 2
    
    def clean_content(self, text):
        # Bersihkan teks
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,!?;:()-]', '', text)
        if 50 <= len(text) <= 400:
            return text.strip()
        return None
    
    def save_wisdom(self, wisdom_list):
        try:
            try:
                with open('islamic_knowledge.json', 'r', encoding='utf-8') as f:
                    knowledge = json.load(f)
            except:
                knowledge = {
                    "sabar": [
                        "Sabar itu cahaya - HR Muslim",
                        "Allah menyukai orang-orang yang sabar - QS Ali Imran: 146"
                    ],
                    "syukur": [
                        "Bersyukurlah kepada Allah - QS Ibrahim: 7"
                    ],
                    "shalat": [
                        "Shalat adalah tiang agama"
                    ],
                    "tasawuf": [],
                    "akhlak": [],
                    "umum": []
                }
            
            for wisdom in wisdom_list:
                wisdom_lower = wisdom.lower()
                added = False
                
                # Categorize wisdom
                categories = {
                    'sabar': ['sabar', 'bersabar', 'kesabaran'],
                    'syukur': ['syukur', 'bersyukur'],
                    'shalat': ['shalat', 'sholat', 'sembahyang'],
                    'tasawuf': ['tasawuf', 'sufi', 'zikir', 'hati'],
                    'akhlak': ['akhlak', 'moral', 'etika', 'perilaku']
                }
                
                for category, keywords in categories.items():
                    if any(keyword in wisdom_lower for keyword in keywords):
                        if wisdom not in knowledge[category]:
                            knowledge[category].append(wisdom)
                            added = True
                            print(f"📁 Categorized as {category}: {wisdom[:50]}...")
                            break
                
                if not added and wisdom not in knowledge["umum"]:
                    knowledge["umum"].append(wisdom)
                    print(f"📁 Categorized as umum: {wisdom[:50]}...")
            
            with open('islamic_knowledge.json', 'w', encoding='utf-8') as f:
                json.dump(knowledge, f, ensure_ascii=False, indent=2)
                
            print(f"💾 Saved {len(wisdom_list)} wisdom to knowledge base!")
                
        except Exception as e:
            print(f"❌ Save error: {e}")

# ===== JALANKAN AUTO-LEARNING =====
ai_learner = BackgroundLearner()
ai_learner.start_auto_learning()

# ===== KNOWLEDGE BASE =====
def load_knowledge():
    try:
        with open('islamic_knowledge.json', 'r', encoding='utf-8') as f:
            knowledge = json.load(f)
            print(f"📚 Knowledge base loaded: {sum(len(v) for v in knowledge.values())} wisdom")
            return knowledge
    except Exception as e:
        print(f"❌ Error loading knowledge: {e}")
        return {
            "sabar": ["Sabar itu cahaya - HR Muslim"],
            "syukur": ["Bersyukurlah kepada Allah - QS Ibrahim: 7"],
            "shalat": ["Shalat adalah tiang agama"],
            "tasawuf": [],
            "akhlak": [],
            "umum": []
        }

# ===== STATUS ENDPOINT =====
@app.route('/api/status')
def learning_status():
    knowledge = load_knowledge()
    total_wisdom = sum(len(wisdom_list) for wisdom_list in knowledge.values())
    
    return jsonify({
        "status": "AI sedang aktif belajar di background",
        "learned_rounds": ai_learner.learned_count,
        "total_knowledge": total_wisdom,
        "categories": {cat: len(wisdom) for cat, wisdom in knowledge.items()},
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# ===== CHAT INTERFACE =====
@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Nur AI - ChatGPT-like</title>
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
                padding: 20px;
                text-align: center;
            }
            .header h1 {
                font-size: 2em;
                margin-bottom: 5px;
            }
            .status-bar {
                background: #e8f5e8;
                padding: 10px 20px;
                border-bottom: 1px solid #c8e6c9;
                display: flex;
                justify-content: space-between;
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
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌙 Nur AI</h1>
                <p>ChatGPT-like dengan Auto Learning di Background</p>
            </div>
            
            <div class="status-bar">
                <strong>🔄 Status:</strong> 
                <span id="learningStatus">Aktif belajar dari nu.or.id</span>
                • <span id="knowledgeCount">Loading...</span>
            </div>
            
            <div class="chat-container" id="chatContainer">
                <div class="message ai-message">
                    <strong>Assalamu'alaikum! 🌟</strong><br>
                    Saya Nur AI. Saya sedang belajar otomatis dari website NU Online (nu.or.id) tentang tasawuf dan akhlak!
                </div>
            </div>
            
            <div class="input-container">
                <input type="text" id="messageInput" placeholder="Tanya tentang sabar, tasawuf, akhlak..." autocomplete="off">
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

            // Update learning status
            async function updateLearningStatus() {
                try {
                    const response = await fetch('/api/status');
                    const data = await response.json();
                    
                    document.getElementById('learningStatus').textContent = data.status;
                    document.getElementById('knowledgeCount').textContent = 
                        `Total: ${data.total_knowledge} wisdom`;
                } catch (error) {
                    console.log('Gagal update status');
                }
            }

            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            // Update status setiap 30 detik
            setInterval(updateLearningStatus, 30000);
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
        
        if any(greet in user_lower for greet in ['halo', 'hai', 'assalamu', 'hello', 'p']):
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
            response = "Saya Nur AI, assistant Islami yang terus belajar dari NU Online!"
            
        else:
            if knowledge['umum']:
                import random
                response = random.choice(knowledge['umum'])
            else:
                default_responses = [
                    "Pertanyaan yang bagus! Saya sedang belajar dari NU Online tentang tasawuf dan akhlak.",
                    "Coba tanya tentang sabar, tasawuf, atau akhlak. Saya baru belajar dari nu.or.id!",
                    "Menarik! Saya akan terus belajar untuk jawab pertanyaan seperti ini."
                ]
                import random
                response = random.choice(default_responses)

        return jsonify({
            "response": response,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
    except Exception as e:
        return jsonify({"response": f"Maaf terjadi error: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Server running on: http://localhost:{port}")
    print("🎯 Auto-learning aktif di background!")
    print("📚 Sumber belajar: nu.or.id (tasawuf & akhlak)")
    print("⏹️  Tekan Ctrl+C untuk stop")
    app.run(host='0.0.0.0', port=port, debug=False)
