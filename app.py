from flask import Flask, request, jsonify, render_template
from response_engine import ResponseEngine
import os
from datetime import datetime

app = Flask(__name__)

# Initialize the SMART engine
print("🌙 Loading Nur AI Smart Engine...")
ai_engine = ResponseEngine()
print("✅ Nur AI Smart Engine Ready!")

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
        
        # Use the SMART engine dengan error handling
        ai_response = ai_engine.generate_response(user_message)
        
        return jsonify(ai_response)
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "response": "Maaf, ada gangguan sebentar. Mari kita coba lagi...",
            "emotion": "netral", 
            "timestamp": datetime.now().strftime("%H:%M")
        })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "service": "Nur AI Smart Version",
        "features": ["emotion_detection", "islamic_knowledge", "personalized_responses"]
    })

# Vercel compatible
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🌙 Nur AI Smart Version Starting...")
    print("📱 Access at: http://localhost:5000")
    print("🧠 Features: Emotion Detection, Islamic Wisdom, Personalized Responses")
    print("⚡ Optimized for Vercel")
    app.run(host='0.0.0.0', port=port, debug=False)
