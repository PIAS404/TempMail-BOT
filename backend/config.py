# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DOMAIN = os.getenv("DOMAIN")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL not found in .env")
if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY not found in .env")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found in .env")
if not DOMAIN:
    raise ValueError("DOMAIN not found in .env")

print(f"✅ Config Loaded - Domain: {DOMAIN}")
