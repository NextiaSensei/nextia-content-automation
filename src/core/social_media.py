import json
from instagrapi import Client as InstagramClient
import tweepy
from config.settings import INSTAGRAM, TWITTER

class MultiPlatformPublisher:
    """Publica contenido en múltiples redes"""
    
    def __init__(self):
        self.instagram = self._init_instagram()
        self.twitter = self._init_twitter()
    
    def _init_instagram(self):
        try:
            ig = InstagramClient()
            ig.login(INSTAGRAM["username"], INSTAGRAM["password"])
            return ig
        except Exception as e:
            print(f"❌ Instagram login error: {e}")
            return None
    
    def _init_twitter(self):
        try:
            auth = tweepy.OAuthHandler("API_KEY", "API_SECRET")
            auth.set_access_token(TWITTER["bearer_token"], "TOKEN_SECRET")
            return tweepy.API(auth)
        except Exception as e:
            print(f"❌ Twitter login error: {e}")
            return None
    
    def post_to_instagram(self, image_path, caption, hashtags=""):
        """Publica imagen en Instagram"""
        try:
            full_caption = f"{caption}\n\n{hashtags}"
            media = self.instagram.photo_upload(image_path, caption=full_caption)
            print(f"✅ Instagram: Publicado exitosamente")
            return media
        except Exception as e:
            print(f"❌ Error Instagram: {e}")
            return None
    
    def post_to_twitter(self, text, image_path=None):
        """Publica en Twitter/X"""
        try:
            if image_path:
                # Sube imagen primero
                media = self.twitter.media_upload(image_path)
                self.twitter.update_status(text, media_ids=[media.id])
            else:
                self.twitter.update_status(text)
            print(f"✅ Twitter: Publicado exitosamente")
        except Exception as e:
            print(f"❌ Error Twitter: {e}")
    
    def publish_batch(self, posts_json, image_dir):
        """Publica lote de posts"""
        with open(posts_json, "r", encoding="utf-8") as f:
            posts = json.load(f)
        
        for post in posts:
            platform = post.get("platform")
            if platform == "instagram":
                image = f"{image_dir}/{post['id']}.png"
                self.post_to_instagram(image, post["texto"], post["hashtags"])
            elif platform == "twitter":
                self.post_to_twitter(post["texto"])
