import requests
import os

print("🔍 TEST STATUS API KEY GEMINI")
print("=" * 50)

API_KEY = "AIzaSyBSPTuqaE2x1TP15lznwhCtSuZ4DfrFEWM"
print(f"Testing API Key: {API_KEY}")

# Test 1: Cek dengan endpoint yang sederhana
print("\n1. Testing dengan endpoint sederhana...")
url1 = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
try:
    response = requests.get(url1, timeout=10)
    print(f"   Models Endpoint: HTTP {response.status_code}")
    if response.status_code == 200:
        print("   ✅ API Key VALID! Bisa akses models")
    else:
        print(f"   ❌ API Key problem: {response.text[:100]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Cek quota/trial status
print("\n2. Testing generateContent dengan prompt sederhana...")
url2 = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
data = {
    "contents": [{
        "parts": [{"text": "Hello"}]
    }]
}
try:
    response = requests.post(url2, json=data, timeout=10)
    print(f"   GenerateContent: HTTP {response.status_code}")
    if response.status_code == 200:
        print("   ✅ GenerateContent BERHASIL!")
    elif response.status_code == 403:
        print("   ❌ QUOTA HABIS atau API Key disabled")
    elif response.status_code == 404:
        print("   ❌ PROJECT TIDAK AKTIF atau region blocked")
    else:
        print(f"   ❌ Unknown error: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 50)
print("📋 DIAGNOSA:")
print("   - API Key: Ada tapi mungkin expired/disabled")
print("   - Kemungkinan: Quota habis, project tidak aktif, atau region restriction")
print("   - Solusi: Buat API Key baru di Google AI Studio")
