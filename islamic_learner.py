import requests
from bs4 import BeautifulSoup
import re
import time
import json

class IslamicAILearner:
    def __init__(self):
        self.trusted_sources = ["islam.nu.or.id", "muslim.or.id", "konsultasisyariah.com"]
        self.knowledge_file = "islamic_knowledge.json"
        
    def safe_learn(self, url):
        try:
            if not any(trusted in url for trusted in self.trusted_sources):
                return {"error": "❌ URL tidak terpercaya"}
            
            time.sleep(1)
            content = self.extract_islamic_content(url)
            if content:
                self.save_knowledge(content)
                return {"success": f"✅ Berhasil belajar {len(content)} wisdom!", "content": content}
            else:
                return {"error": "❌ Tidak ada konten Islami"}
            
        except Exception as e:
            return {"error": f"❌ Gagal: {str(e)}"}
    
    def extract_islamic_content(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, timeout=10, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            islamic_wisdom = []
            content_selectors = ['article', '.post-content', '.entry-content', 'main']
            
            for selector in content_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text().strip()
                    paragraphs = text.split('\n')
                    
                    for paragraph in paragraphs:
                        paragraph = paragraph.strip()
                        if len(paragraph) > 50 and self.is_islamic_content(paragraph):
                            wisdom = self.clean_content(paragraph)
                            if wisdom and wisdom not in islamic_wisdom:
                                islamic_wisdom.append(wisdom)
            
            return islamic_wisdom[:3]
            
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def is_islamic_content(self, text):
        islamic_keywords = ['allah', 'rasulullah', 'islam', 'muslim', 'quran', 'hadits', 'sabar', 'syukur']
        text_lower = text.lower()
        keyword_count = sum(1 for keyword in islamic_keywords if keyword in text_lower)
        return keyword_count >= 2
    
    def clean_content(self, text):
        text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
        sentences = text.split('.')
        for sentence in sentences:
            if len(sentence) > 30 and self.is_islamic_content(sentence):
                return sentence.strip()[:200]
        return None
    
    def save_knowledge(self, new_wisdom):
        try:
            # Load existing knowledge
            try:
                with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                    knowledge = json.load(f)
            except:
                knowledge = {"sabar": [], "syukur": [], "umum": []}
            
            # Add new wisdom
            for wisdom in new_wisdom:
                wisdom_lower = wisdom.lower()
                if 'sabar' in wisdom_lower:
                    knowledge["sabar"].append(wisdom)
                elif 'syukur' in wisdom_lower:
                    knowledge["syukur"].append(wisdom)
                else:
                    knowledge["umum"].append(wisdom)
            
            # Save back
            with open(self.knowledge_file, 'w', encoding='utf-8') as f:
                json.dump(knowledge, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Save error: {e}")

