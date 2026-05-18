from backend.database import supabase
from datetime import datetime
from typing import List, Optional

# ==================== USER ====================

async def get_or_create_user(telegram_id: int):
    response = supabase.table("users").select("*").eq("telegram_id", telegram_id).execute()
    if response.data:
        return response.data[0]
    new_user = {
        "telegram_id": telegram_id,
        "created_at": datetime.utcnow().isoformat()
    }
    result = supabase.table("users").insert(new_user).execute()
    return result.data[0]

# ==================== USER EMAIL ====================

async def create_user_email(telegram_id: int, email_address: str):
    user = await get_or_create_user(telegram_id)
    new_email = {
        "user_id": user["id"],
        "email_address": email_address.lower(),
        "created_at": datetime.utcnow().isoformat()
    }
    result = supabase.table("user_emails").insert(new_email).execute()
    return result.data[0]

async def get_user_emails(telegram_id: int) -> List[dict]:
    user = await get_or_create_user(telegram_id)
    response = supabase.table("user_emails").select("*").eq("user_id", user["id"]).execute()
    return response.data

async def get_email_by_address(email_address: str):
    response = supabase.table("user_emails").select("*").eq("email_address", email_address.lower()).execute()
    return response.data[0] if response.data else None

# ==================== INCOMING EMAIL ====================

async def save_incoming_email(user_email_id: int, payload: dict):
    email_data = {
        "user_email_id": user_email_id,
        "from_email": payload.get("From", ""),
        "from_name": payload.get("FromName", ""),
        "subject": payload.get("Subject", "No Subject"),
        "text_body": payload.get("TextBody", ""),
        "html_body": payload.get("HtmlBody", ""),
        "message_id": payload.get("MessageID", ""),
        "received_at": datetime.utcnow().isoformat()
    }
    result = supabase.table("emails").insert(email_data).execute()
    return result.data[0]

# ★ নতুন ফাংশন — Inbox দেখানোর জন্য
async def get_inbox_for_user(telegram_id: int) -> List[dict]:
    user = await get_or_create_user(telegram_id)
    user_emails = await get_user_emails(telegram_id)
    
    if not user_emails:
        return []
    
    all_inbox = []
    for ue in user_emails:
        response = supabase.table("emails").select("*").eq("user_email_id", ue["id"]).order("received_at", desc=True).execute()
        all_inbox.extend(response.data)
    
    # সময় অনুযায়ী sort
    all_inbox.sort(key=lambda x: x.get("received_at", ""), reverse=True)
    return all_inbox
