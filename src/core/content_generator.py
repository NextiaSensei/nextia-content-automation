import json
import os
from datetime import datetime
import google.generativeai as genai
from config.settings import GEMINI_API_KEY, GEMINI_MODEL, NICHES

genai.configure(api_key=GEMINI_API_KEY)

class ContentGenerator:
    """Genera contenido automatizado usando Gemini AI"""
    
    def __init__(self, niche="nextia_token"):
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.niche = niche
        self.config = NICHES.get(niche, NICHES["nextia_token"])
    
    def generate_posts(self, quantity=5, content_type="mixed"):
        """
        Genera múltiples posts para redes sociales
        content_type: "motivational", "educational", "viral", "mixed"
        """
        prompt = f"""
        Eres un experto en {self.config['name']}.
        
        Genera exactamente {quantity} posts para redes sociales con:
        - Máximo 280 caracteres para Twitter
        - 150-200 caracteres para Instagram
        - 100-150 caracteres para TikTok
        - Estilo: {content_type}
        - Hashtags relevantes: {', '.join(self.config['hashtags'])}
        - Lenguaje: Profesional, engaging, viral-friendly
        - Incluye call-to-action
        
        IMPORTANTE: Responde SOLO en JSON válido sin markdown.
        
        Formato JSON:
        {{
            "posts": [
                {{
                    "texto": "texto del post",
                    "platform": "instagram|tiktok|twitter|youtube",
                    "hashtags": "hashtags relevantes",
                    "cta": "call to action",
                    "tipo_contenido": "video|carousel|image|story"
                }},
                ...
            ]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result["posts"]
        except json.JSONDecodeError:
            print("❌ Error al parsear JSON de Gemini")
            return []
    
    def generate_video_script(self, topic, duration_seconds=60):
        """Genera script para video con timing"""
        prompt = f"""
        Crea un script de video para {self.config['name']}.
        Tema: {topic}
        Duración: {duration_seconds} segundos
        
        El video tiene DOS PANTALLAS:
        - Pantalla izquierda: Visuals (descripción de qué mostrar)
        - Pantalla derecha: Voiceover (narración)
        
        Formato JSON con timing:
        {{
            "title": "título del video",
            "duration": {duration_seconds},
            "scenes": [
                {{
                    "timestamp": "00:00-00:10",
                    "left_visual": "descripción de visual",
                    "right_voiceover": "texto a narrar"
                }},
                ...
            ]
        }}
        
        Responde SOLO JSON válido.
        """
        
        response = self.model.generate_content(prompt)
        try:
            return json.loads(response.text)
        except:
            return {}
    
    def generate_hashtags(self, text, platform="instagram"):
        """Genera hashtags optimizados por plataforma"""
        prompt = f"""
        Genera 15-20 hashtags relevantes para {platform}.
        Texto base: {text}
        Niche: {self.config['name']}
        
        Responde como JSON:
        {{"hashtags": ["#hashtag1", "#hashtag2", ...]}}
        """
        
        response = self.model.generate_content(prompt)
        try:
            return json.loads(response.text)
        except:
            return {"hashtags": self.config["hashtags"]}

# Test
if __name__ == "__main__":
    gen = ContentGenerator("nextia_token")
    posts = gen.generate_posts(quantity=3, content_type="educational")
    print(json.dumps(posts, indent=2, ensure_ascii=False))
