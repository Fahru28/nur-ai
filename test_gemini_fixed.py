import requests
import os
import json

print("🔧 TEST GEMINI DENGAN URL YANG BENAR")
print("=" * 50)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBSPTuqaE2x1TP15lznwhCtSuZ4DfrFEWM')
print(f"API Key: {GEMINI_API_KEY[:20]}...")

# URL yang BENAR untuk Gemini API
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

headers = {'Content-Type': 'application/json'}
data = {
    "contents": [{
        "parts": [{"text": "Hai, respon dengan salam Islami singkat!"}]
    }]
}

print(f"URL: {url[:80]}...")
print("Mengirim request...")

try:
    response = requests.post(url, headers=headers, json=data, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        ai_response = result['candidates'][0]['content']['parts'][0]['text']
        print("🎉 BERHASIL! Gemini merespons:")
        print(f"   {ai_response}")
    else:
        print(f"❌ GAGAL: HTTP {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
except Exception as e:
    print(f"❌ ERROR: {str(e)}")

# Test alternatif URL
print("\n" + "=" * 50)
print("TEST ALTERNATIF URL...")

# Coba URL alternatif
url_alt = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
data_alt = {
    "contents": [{
        "parts": [{"text": "Test"}]
    }]
}

try:
    response = requests.post(
        url_alt, 
        headers=headers, 
        json=data_alt,
        params={"key": GEMINI_API_KEY},
        timeout=10
    )
    print(f"Alternatif URL Status: {response.status_code}")
except Exception as e:
    print(f"Alternatif URL Error: {str(e)}")
