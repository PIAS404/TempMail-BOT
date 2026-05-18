from supabase import create_client, Client
from backend.config import SUPABASE_URL, SUPABASE_KEY

# Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("✅ Supabase Connected Successfully!")
