from flask import Flask, request, jsonify, render_template
from response_engine_enhanced import EnhancedResponseEngine
import os
from datetime import datetime

app = Flask(__name__)
ai_engine = EnhancedResponseEngine()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                "response": "Maaf, pesan tidak boleh kosong...",
                "emotion": "netral",
                "timestamp": datetime.now().strftime("%H:%M")
            })
        
        ai_response = ai_engine.generate_response(user_message)
        return jsonify(ai_response)
        
    except Exception as e:
        return jsonify({
            "response": "Maaf, terjadi kesalahan. Silakan coba lagi...",
            "emotion": "netral", 
            "timestamp": datetime.now().strftime("%H:%M")
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🌙 Nur AI Enhanced Version Starting...")
    print("📱 Access at: http://localhost:5000")
    print("🎯 Better intent recognition!")
    app.run(host='0.0.0.0', port=port, debug=False)
