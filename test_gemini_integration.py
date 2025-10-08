import requests
import os
import json
from datetime import datetime

print("🧪 TEST INTEGRASI GEMINI API")
print("=" * 50)

# Test 1: Cek Environment Variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBSPTuqaE2x1TP15lznwhCtSuZ4DfrFEWM')
print(f"1. API Key: {'✅ Ditemukan' if GEMINI_API_KEY else '❌ Tidak ditemukan'}")
print(f"   Key: {GEMINI_API_KEY[:20]}...")

# Test 2: Test Koneksi ke Gemini API
def test_gemini_connection():
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": "Hai, respon dengan: 'TEST BERHASIL - Gemini Connected!'"}]
        }]
    }
    
    try:
        start_time = datetime.now()
        response = requests.post(url, headers=headers, json=data, timeout=10)
        end_time = datetime.now()
        
        response_time = (end_time - start_time).total_seconds()
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['candidates'][0]['content']['parts'][0]['text']
            print(f"2. Koneksi Gemini: ✅ BERHASIL")
            print(f"   Response Time: {response_time:.2f} detik")
            print(f"   AI Response: {ai_response}")
            return True, ai_response
        else:
            print(f"2. Koneksi Gemini: ❌ GAGAL (HTTP {response.status_code})")
            return False, None
            
    except Exception as e:
        print(f"2. Koneksi Gemini: ❌ ERROR - {str(e)}")
        return False, None

# Test 3: Test dengan berbagai input
def test_various_inputs():
    test_cases = [
        "Hai",
        "Aku sedih",
        "Terima kasih",
        "Hari apa sekarang?",
        "Kamu siapa?",
        "Beri aku motivasi"
    ]
    
    print("\n3. Test Berbagai Input:")
    print("-" * 30)
    
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    for i, test_input in enumerate(test_cases, 1):
        prompt = f"""
        Anda adalah Nur AI - asisten spiritual Islami.
        Personality: Lembut, Islami, awali dengan salam.
        Respons 1-2 kalimat saja untuk: "{test_input}"
        """
        
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                ai_response = result['candidates'][0]['content']['parts'][0]['text']
                print(f"   {i}. '{test_input}' → ✅: {ai_response[:50]}...")
            else:
                print(f"   {i}. '{test_input}' → ❌: HTTP {response.status_code}")
        except Exception as e:
            print(f"   {i}. '{test_input}' → ❌: {str(e)}")

# Jalankan test
print("\n" + "=" * 50)
success, response = test_gemini_connection()

if success:
    print("\n🎉 SEMUA TEST BERHASIL! Gemini terintegrasi dengan baik!")
    print("   Semua input seharusnya dapat respons dari AI")
else:
    print("\n❌ ADA MASALAH DENGAN INTEGRASI GEMINI!")
    print("   Periksa: API Key, koneksi internet, atau quota Gemini")

# Test berbagai input jika koneksi berhasil
if success:
    test_various_inputs()

print("\n" + "=" * 50)
print("📊 SUMMARY:")
print(f"   - API Key: {'✅ Ready' if GEMINI_API_KEY else '❌ Missing'}")
print(f"   - Gemini Connection: {'✅ Working' if success else '❌ Failed'}")
print(f"   - Response Time: {'✅ Fast' if success and 'TEST BERHASIL' in response else '❌ Slow/Error'}")
