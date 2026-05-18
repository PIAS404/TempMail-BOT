from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")
    DOMAIN: str = os.getenv("DOMAIN", "yourdomain.com")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")


settings = Settings()

# Quick check
if not settings.TELEGRAM_TOKEN:
    print("⚠️ Warning: TELEGRAM_TOKEN is missing in .env")
if not settings.DOMAIN:
    print("⚠️ Warning: DOMAIN is missing in .env")
