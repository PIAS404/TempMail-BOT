# backend/config.py

# ================== তোমার তথ্য এখানে দাও ==================

SUPABASE_URL = "https://vziagzcedlrfjxxjynvi.supabase.co"   # তোমার Supabase Project URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ6aWFnemNlZGxyZmp4eGp5bnZpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkxMTY1MTcsImV4cCI6MjA5NDY5MjUxN30.DHUbjjScWbIxvozh1EgbAs0mPPzxlB-ShKSyzMOEwUQ"       # তোমার anon public key

TELEGRAM_TOKEN = "8280327644:AAFEwkpyicJ4sbNHsahhXbJn5FnyRNqp19s"                                         # এখানে তোমার Telegram Bot Token দাও

DOMAIN = "piasx.top"                                   # তোমার ডোমেইন

# =========================================================

import os
from dotenv import load_dotenv

load_dotenv()

# .env ফাইল থাকলে তার প্রায়োরিটি বেশি
if os.getenv("SUPABASE_URL"):
    SUPABASE_URL = os.getenv("SUPABASE_URL")
if os.getenv("SUPABASE_KEY"):
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if os.getenv("TELEGRAM_TOKEN"):
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if os.getenv("DOMAIN"):
    DOMAIN = os.getenv("DOMAIN")


print(f"✅ Config Loaded - Domain: {DOMAIN}")
