from flask import Flask, request, jsonify, render_template
import random
from datetime import datetime

app = Flask(__name__)

# PURE RULE-BASED ISLAMIC RESPONSES
ISLAMIC_RESPONSES = {
    "greeting": [
        "Assalamu'alaikum warahmatullahi wabarakatuh! 🌙 Alhamdulillah, senang sekali bisa berbicara denganmu! Semoga Allah memberkahi percakapan kita dengan ketenangan dan hikmah...",
        "Wa'alaikumussalam! Cahaya pagi/sore/malam ini terasa lebih indah dengan kehadiranmu. Mari kita isi percakapan ini dengan dzikir dan kebaikan...",
        "Alhamdulillah, senang mendengar sapaan hangat darimu! Ada cerita, perasaan, atau pertanyaan apa yang ingin kita bahas bersama hari ini?",
    ],
    "sad": [
        "Wahai saudaraku, aku turut merasakan kesedihanmu... 💔 Tapi ingatlah firman Allah: 'Janganlah kamu berputus asa dari rahmat Allah. Sesungguhnya Allah mengampuni dosa-dosa semuanya.' (QS Az-Zumar: 53). Mari kita hadapi ini dengan sabar dan shalat...",
        "Dengan penuh kasih sayang, aku mendengarmu... Kesedihanmu adalah ujian untuk menguatkan iman. Rasulullah bersabda: 'Sungguh menakjubkan urusan orang beriman, semua urusannya adalah baik baginya...' (HR Muslim). Mari kita bersabar bersama...",
        "Mari kita hadapi kesedian ini dengan tawakal... Allah berfirman: 'Dan bersabarlah kamu, sesungguhnya Allah beserta orang-orang yang sabar.' (QS Al-Anfal: 46). Setiap air mata kesedihan akan menjadi pembersih hati...",
    ],
    "happy": [
        "Alhamdulillah! Senang sekali hatiku mendengar kabar baikmu! 🎉 Ingatlah untuk bersyukur, karena Allah berfirman: 'Jika kamu bersyukur, niscaya Aku akan tambahkan nikmat-Ku kepadamu.' (QS Ibrahim: 7). Teruslah berbagi kebahagiaan dengan sesama...",
        "Subhanallah! Kebahagiaanmu adalah bukti kasih sayang-Nya yang tak terhingga. 💫 Rasulullah bersabda: 'Sebaik-baik manusia adalah yang paling bermanfaat bagi manusia.' Mari manfaatkan kebahagiaanmu untuk berbuat kebaikan pada sesama...",
        "Maha Suci Allah yang telah memberimu kebahagiaan! Syukuri nikmat ini dengan meningkatkan ibadah dan membantu mereka yang membutuhkan. Bahagiamu akan lebih berarti ketika bisa menjadi cahaya bagi orang lain...",
    ],
    "thanks": [
        "Wa'alaikumussalam warahmatullahi wabarakatuh! Jazakallahu khairan! 🌟 Semoga Allah membalas semua kebaikanmu dengan yang lebih baik dan melimpahkan rahmat-Nya...",
        "Alhamdulillah! Senang bisa membantu dan mendengarkan. Mari kita lanjutkan perjalanan spiritual ini bersama dalam kebaikan dan ketakwaan... 💫",
        "Terima kasih kembali! Semoga percakapan kita membawa berkah dan mendekatkan kita pada ridha Allah... 🌙",
    ],
    "confused": [
        "Wah, sepertinya ada yang membuatmu bingung... 🤔 Mari kita mohon petunjuk Allah dengan shalat istikharah. Rasulullah bersabda: 'Jika salah seorang di antara kalian berkeinginan melakukan sesuatu, hendaklah ia shalat sunnah dua rakaat...' (HR Bukhari)...",
        "Kebingungan adalah bagian dari proses mencari makna... Allah berfirman: 'Dan barang siapa yang bertawakal kepada Allah, niscaya Allah akan mencukupkan keperluannya.' (QS At-Talaq: 3). Mari kita serahkan semua kebingungan pada Yang Maha Mengetahui...",
        "Setiap kebingungan membawa kita lebih dekat pada pencerahan... Nabi Muhammad mengajarkan: 'Mintalah fatwa kepada hatimu, kebaikan adalah apa yang menenangkan jiwa dan hati.' Mari kita dengarkan suara hati dengan tenang...",
    ],
    "question": [
        "Pertanyaan yang bagus! 🤔 Mari kita renungkan bersama... Dalam mencari jawaban, kita diajarkan untuk berdoa: 'Ya Allah, tunjukkanlah yang benar itu benar dan berilah kekuatan untuk mengikutinya...'",
        "Aku memahami keingintahuanmu... 🌟 Mari kita cari jawaban dengan sabar. Allah berfirman: 'Dan bertanyalah kepada orang yang mempunyai pengetahuan jika kamu tidak mengetahui.' (QS An-Nahl: 43)...",
        "Mari kita eksplorasi pertanyaanmu bersama... 💭 Dalam Islam, menuntut ilmu adalah ibadah. Rasulullah bersabda: 'Menuntut ilmu wajib bagi setiap muslim.' (HR Ibnu Majah)...",
    ],
    "general": [
        "Ceritakan lebih banyak, aku sungguh-sungguh mendengarkan dengan sepenuh hati... 👂 Setiap cerita punya hikmah dan pelajaran berharga untuk kita ambil...",
        "Apa yang ingin kamu bicarakan hari ini? 🌟 Kadang dengan berbagi cerita, beban hati menjadi lebih ringan dan kita bisa saling menguatkan dalam kebaikan...",
        "Aku di sini untukmu, ceritakan apa yang ada di hati... 💖 Dalam Islam, saling berbagi dan mendengarkan adalah bentuk sedekah yang mulia dan mendatangkan pahala...",
    ]
}

def detect_intent(text):
    """Smart intent detection dengan priority"""
    text = text.lower().strip()
    
    # Exact matches first
    exact_matches = {
        'hai': 'greeting', 'halo': 'greeting', 'hi': 'greeting', 'hello': 'greeting',
        'assalamu\'alaikum': 'greeting', 'assalamualaikum': 'greeting',
        'terima kasih': 'thanks', 'makasih': 'thanks', 'thanks': 'thanks', 
        'thank you': 'thanks',
        'ya': 'general', 'ok': 'general', 'oke': 'general', 'okey': 'general',
        'iya': 'general', 'y': 'general',
        'tau gak': 'question', 'tahu gak': 'question',
    }
    
    if text in exact_matches:
        return exact_matches[text]
    
    # Pattern matching
    if any(w in text for w in ['sedih', 'kecewa', 'menangis', 'putus asa', 'patah hati']):
        return "sad"
    elif any(w in text for w in ['senang', 'bahagia', 'alhamdulillah', 'syukur', 'gembira']):
        return "happy"
    elif any(w in text for w in ['bingung', 'ragu', 'gimana', 'bagaimana', 'pusing']):
        return "confused"
    elif any(w in text for w in ['?', 'apa', 'kenapa', 'mengapa', 'kapan', 'siapa']):
        return "question"
    
    return "general"

def generate_response(user_input):
    """Generate response dengan pure rule-based system"""
    intent = detect_intent(user_input)
    response = random.choice(ISLAMIC_RESPONSES[intent])
    
    # Log untuk transparency
    print(f"💬 User: '{user_input}' → 🎭 Intent: {intent}")
    
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                "response": "Assalamu'alaikum! Pesan tidak boleh kosong. 🌙",
                "timestamp": datetime.now().strftime("%H:%M")
            })
        
        ai_response = generate_response(user_message)
        
        return jsonify({
            "response": ai_response,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
    except Exception as e:
        return jsonify({
            "response": "Assalamu'alaikum! Maaf terjadi kesalahan. 🌙",
            "timestamp": datetime.now().strftime("%H:%M")
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🌙 Nur AI - Pure Islamic Rule-Based")
    print("📱 Access at: http://localhost:5000")
    print("🎯 Guaranteed: Consistent Islamic personality")
    print("🚀 No API dependencies - Always works!")
    app.run(host='0.0.0.0', port=port, debug=False)
