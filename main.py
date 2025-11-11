#!/usr/bin/env python3
import sys
import logging
from datetime import datetime
from src.core.content_generator import ContentGenerator
from src.core.video_creator import DualScreenVideoCreator
from src.core.social_media import MultiPlatformPublisher
from config.settings import LOGS_DIR, NICHES, DEBUG

# Setup Logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{LOGS_DIR}/nextia_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NextiaContentAutomation:
    """Orquestador principal del sistema"""
    
    def __init__(self, niche="nextia_token"):
        self.niche = niche
        self.generator = ContentGenerator(niche)
        self.video_creator = DualScreenVideoCreator()
        self.publisher = MultiPlatformPublisher()
        logger.info(f"✅ Sistema inicializado para niche: {niche}")
    
    def run_full_pipeline(self, num_posts=5):
        """Ejecuta el pipeline completo: generar -> crear -> publicar"""
        logger.info(f"🚀 Iniciando pipeline completo - {num_posts} posts")
        
        try:
            # PASO 1: Generar contenido
            logger.info("📝 Generando contenido con IA...")
            posts = self.generator.generate_posts(quantity=num_posts)
            
            if not posts:
                logger.error("❌ No se generó contenido")
                return False
            
            logger.info(f"✅ {len(posts)} posts generados")
            
            # PASO 2: Crear videos (opcional)
            logger.info("🎥 Creando videos con doble pantalla...")
            for i, post in enumerate(posts):
                if post.get("tipo_contenido") == "video":
                    script = self.generator.generate_video_script(post["texto"])
                    video_name = f"video_{self.niche}_{i}.mp4"
                    self.video_creator.create_dual_screen_video(script, video_name)
            
            # PASO 3: Publicar
            logger.info("📤 Publicando en redes sociales...")
            self.publisher.publish_batch(posts)
            
            logger.info("🎉 Pipeline completado exitosamente")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error en pipeline: {e}", exc_info=True)
            return False
    
    def generate_only(self, num_posts=5):
        """Solo genera contenido, no publica"""
        posts = self.generator.generate_posts(quantity=num_posts)
        return posts

def main():
    print("""
    ╔════════════════════════════════════════╗
    ║  NEXTIA CONTENT AUTOMATION SYSTEM      ║
    ║  v1.0 - Professional Automation Tool  ║
    ╚════════════════════════════════════════╝
    """)
    
    # Selecciona niche
    print("\n📚 Nichos disponibles:")
    for i, (key, niche) in enumerate(NICHES.items(), 1):
        print(f"  {i}. {niche['name']} ({key})")
    
    choice = input("\n🔹 Selecciona niche (1-4): ").strip()
    niche_list = list(NICHES.keys())
    
    if choice.isdigit() and 1 <= int(choice) <= len(niche_list):
        selected_niche = niche_list[int(choice) - 1]
    else:
        selected_niche = "nextia_token"
    
    # Crea instancia
    automation = NextiaContentAutomation(niche=selected_niche)
    
    # Menú
    print(f"\n✅ Niche seleccionado: {NICHES[selected_niche]['name']}")
    print("\n📋 Opciones:")
    print("  1. Generar contenido (solo)")
    print("  2. Generar + Crear videos")
    print("  3. Generar + Publicar (Full Pipeline)")
    
    option = input("\n🔹 Selecciona opción: ").strip()
    
    if option == "1":
        posts = automation.generate_only(num_posts=5)
        print("\n📝 Contenido generado:")
        for post in posts:
            print(f"  - {post['texto'][:80]}...")
    
    elif option == "2":
        automation.run_full_pipeline(num_posts=5)
    
    elif option == "3":
        automation.run_full_pipeline(num_posts=5)
    
    else:
        print("❌ Opción inválida")
        sys.exit(1)

if __name__ == "__main__":
    main()
