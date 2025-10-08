from flask import Flask, request, jsonify, render_template
from ai_engine_advanced import AdvancedNurAI
import os
from datetime import datetime

app = Flask(__name__)

# Initialize the ADVANCED engine
print("🌙 Loading Nur AI Advanced Engine...")
ai_engine = AdvancedNurAI()
print("✅ Nur AI Advanced Engine Ready!")
print("🧠 Features: Conversation Memory, Context Awareness, Personalization")

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
                "emotion": "neutral",
                "timestamp": datetime.now().strftime("%H:%M")
            })
        
        # Use the ADVANCED engine
        ai_response = ai_engine.generate_response(user_message)
        
        return jsonify(ai_response)
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "response": "Maaf, ada gangguan sebentar. Mari kita coba lagi...",
            "emotion": "neutral", 
            "timestamp": datetime.now().strftime("%H:%M")
        })

@app.route('/api/conversation/summary')
def conversation_summary():
    """Endpoint to get conversation summary"""
    try:
        summary = ai_engine.get_conversation_summary()
        return jsonify(summary)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "service": "Nur AI Advanced Version",
        "features": [
            "conversation_memory", 
            "context_awareness", 
            "personalized_responses",
            "advanced_emotion_detection"
        ],
        "conversation_count": ai_engine.user_profile["conversation_count"]
    })

# Vercel compatible
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🌙 Nur AI Advanced Version Starting...")
    print("📱 Access at: http://localhost:5000")
    print("🧠 Smart Features: Memory, Context, Personalization")
    print("⚡ Optimized for Vercel")
    app.run(host='0.0.0.0', port=port, debug=False)
