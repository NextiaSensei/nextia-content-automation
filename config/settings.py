import os
from dotenv import load_dotenv

load_dotenv()

# ============ GEMINI AI CONFIG ============
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# ============ SOCIAL MEDIA CREDENTIALS ============
INSTAGRAM = {
    "username": os.getenv("INSTAGRAM_USERNAME"),
    "password": os.getenv("INSTAGRAM_PASSWORD"),
    "account_id": os.getenv("INSTAGRAM_ACCOUNT_ID")
}

FACEBOOK = {
    "access_token": os.getenv("FACEBOOK_ACCESS_TOKEN"),
    "page_id": os.getenv("FACEBOOK_PAGE_ID")
}

TIKTOK = {
    "access_token": os.getenv("TIKTOK_ACCESS_TOKEN"),
    "user_id": os.getenv("TIKTOK_USER_ID")
}

YOUTUBE = {
    "api_key": os.getenv("YOUTUBE_API_KEY"),
    "channel_id": os.getenv("YOUTUBE_CHANNEL_ID")
}

TWITTER = {
    "bearer_token": os.getenv("TWITTER_BEARER_TOKEN"),
    "user_id": os.getenv("TWITTER_USER_ID")
}

TELEGRAM = {
    "bot_token": os.getenv("TELEGRAM_BOT_TOKEN"),
    "channel_id": os.getenv("TELEGRAM_CHANNEL_ID")
}

REDDIT = {
    "client_id": os.getenv("REDDIT_CLIENT_ID"),
    "client_secret": os.getenv("REDDIT_CLIENT_SECRET")
}

# ============ PATHS ============
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
VIDEO_OUTPUT = os.path.join(OUTPUT_DIR, "videos")
IMAGE_OUTPUT = os.path.join(OUTPUT_DIR, "images")

# Create dirs if not exist
for dir_path in [VIDEO_OUTPUT, IMAGE_OUTPUT, LOGS_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# ============ LOGGING ============
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEBUG = os.getenv("DEBUG", "False") == "True"

# ============ CONTENT CONFIG ============
NICHES = {
    "nextia_token": {
        "name": "Nextia Token & Crypto",
        "hashtags": ["#NextiaToken", "#Crypto", "#Web3", "#BlockChain"],
        "platforms": ["instagram", "tiktok", "youtube", "twitter"]
    },
    "marketing_digital": {
        "name": "Marketing Digital",
        "hashtags": ["#MarketingDigital", "#Social", "#Content"],
        "platforms": ["instagram", "facebook", "linkedin", "tiktok"]
    },
    "psicologia": {
        "name": "Psicología Aplicada",
        "hashtags": ["#Psicologia", "#SaludMental", "#Bienestar"],
        "platforms": ["instagram", "tiktok", "youtube"]
    },
    "trading": {
        "name": "Trading & Finanzas",
        "hashtags": ["#Trading", "#Finanzas", "#Inversión"],
        "platforms": ["tiktok", "youtube", "twitter"]
    }
}

# ============ MONETIZATION ============
MONETIZATION_STRATEGIES = {
    "youtube": {
        "min_subscribers": 1000,
        "min_watch_hours": 4000,
        "revenue_share": 0.55
    },
    "tiktok": {
        "min_followers": 5000,
        "min_monthly_views": 100000,
        "fund_range": "$0.02 - $0.04 per 1000 views"
    },
    "instagram": {
        "sponsorship": "Brands partnerships",
        "affiliate": "Product links"
    }
}

