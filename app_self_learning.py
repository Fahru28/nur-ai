from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime
import os
import json

app = Flask(__name__)

# KNOWLEDGE BASE YANG BISA TUMBUH
ISLAMIC_KNOWLEDGE_FILE = "islamic_knowledge.json"

def load_knowledge():
    """Load knowledge dari file"""
    try:
        with open(ISLAMIC_KNOWLEDGE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        # Default knowledge
        return {
            "sabar": ["Rasulullah bersabda: 'Sabar itu cahaya' (HR Muslim)"],
            "syukur": ["Allah berfirman: 'Jika kamu bersyukur, niscaya Aku akan tambahkan nikmat-Ku' (QS Ibrahim: 7)"]
        }

def save_knowledge(knowledge):
    """Save knowledge ke file"""
    with open(ISLAMIC_KNOWLEDGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(knowledge, f, ensure_ascii=False, indent=2)

def learn_from_urls(urls):
    """AI belajar dari list URL"""
    knowledge = load_knowledge()
    new_learned = 0
    
    for url in urls:
        try:
            print(f"📚 Learning from: {url}")
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract paragraphs dengan konten Islami
            paragraphs = soup.find_all('p')
            
            for p in paragraphs:
                text = p.get_text().strip()
                if len(text) > 50:  # Minimal 50 karakter
                    # Cari topik dalam teks
                    topics = ['sabar', 'syukur', 'taubat', 'shalat', 'puasa', 'zakat', 'ikhlas', 'tawakal']
                    
                    for topic in topics:
                        if topic in text.lower():
                            if topic not in knowledge:
                                knowledge[topic] = []
                            
                            # Tambah jika belum ada
                            if text not in knowledge[topic]:
                                knowledge[topic].append(text[:300])  # Simpan 300 karakter
                                new_learned += 1
                                print(f"➕ Learned: {topic} - {text[:50]}...")
            
        except Exception as e:
            print(f"❌ Error learning from {url}: {e}")
    
    if new_learned > 0:
        save_knowledge(knowledge)
        print(f"🎉 Learned {new_learned} new wisdom!")
    
    return knowledge

def get_ai_response(user_input, knowledge):
    """Generate response dari knowledge yang dipelajari"""
    user_input = user_input.lower()
    
    # Cari di knowledge base
    for topic, wisdom_list in knowledge.items():
        if topic in user_input and wisdom_list:
            return random.choice(wisdom_list)
    
    # Fallback
    fallback_responses = [
        "Aku masih belajar tentang itu. Mari kita cari hikmah bersama...",
        "Pertanyaan yang bagus! Aku akan terus belajar untuk bisa memberikan jawaban yang lebih baik.",
        "Semoga Allah memberikan kita pemahaman tentang hal ini. Mari kita terus mencari ilmu..."
    ]
    return random.choice(fallback_responses)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        knowledge = load_knowledge()
        
        if not user_message:
            return jsonify({"response": "Assalamu'alaikum! Pesan tidak boleh kosong. 🌙"})
        
        # Jika user minta belajar dari URL
        if user_message.startswith('http'):
            urls = [user_message]
            knowledge = learn_from_urls(urls)
            ai_response = "Terima kasih! Aku sudah mempelajari konten dari URL tersebut. 🌟"
        else:
            ai_response = get_ai_response(user_message, knowledge)
        
        return jsonify({
            "response": ai_response,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
    except Exception as e:
        return jsonify({"response": "Assalamu'alaikum! Maaf terjadi kesalahan. 🌙"})

@app.route('/api/learn', methods=['POST'])
def learn():
    """Endpoint untuk menambah knowledge dari URL"""
    try:
        data = request.json
        urls = data.get('urls', [])
        
        if not urls:
            return jsonify({"error": "No URLs provided"})
        
        knowledge = learn_from_urls(urls)
        
        return jsonify({
            "status": "success",
            "learned_count": len(knowledge),
            "message": f"Berhasil belajar dari {len(urls)} URL"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    # Load initial knowledge
    knowledge = load_knowledge()
    print(f"📚 Initial knowledge: {len(knowledge)} topics")
    
    port = int(os.environ.get('PORT', 5000))
    print("🌙 Nur AI - Self Learning Version")
    print("📱 Access at: http://localhost:5000")
    app.run(host='0.0.0.0', port=port, debug=False)
