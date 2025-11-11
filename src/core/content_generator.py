import json
import os
from datetime import datetime
import google.generativeai as genai
from config.settings import GEMINI_API_KEY, GEMINI_MODEL, NICHES

genai.configure(api_key=GEMINI_API_KEY)

class ContentGenerator:
    def __init__(self, niche="nextia_token"):
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.niche = niche
        self.config = NICHES.get(niche, NICHES["nextia_token"])
    
    def generate_posts(self, quantity=5, content_type="mixed"):
        prompt = f"Eres experto en {self.config['name']}. Genera {quantity} posts. Responde solo JSON valido con formato posts array"
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            result = json.loads(text)
            return result.get("posts", [])
        except:
            return self._default_posts(quantity)
    
    def _default_posts(self, quantity):
        posts = [
            {"texto": "Nextia Token Web3", "platform": "instagram", "hashtags": "#token", "cta": "Unete", "tipo": "image"},
            {"texto": "Trading IA", "platform": "tiktok", "hashtags": "#trading", "cta": "Ver", "tipo": "video"},
        ]
        return posts[:quantity]
    
    def generate_video_script(self, topic, duration_seconds=60):
        return {"title": topic, "duration": duration_seconds, "scenes": []}
