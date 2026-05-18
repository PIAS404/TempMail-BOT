from fastapi import APIRouter, Request, HTTPException
from backend.database import supabase
from backend.crud import get_email_by_address, save_incoming_email
from backend.config import TELEGRAM_TOKEN
import httpx

router = APIRouter()

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

async def send_telegram_notification(telegram_id: int, payload: dict):
    """ইউজারকে Telegram-এ নোটিফিকেশন পাঠাবে"""
    from_name = payload.get("FromName", "Unknown")
    from_email = payload.get("From", "Unknown")
    subject = payload.get("Subject", "No Subject")
    text_body = payload.get("TextBody", "")[:500]  # প্রথম ৫০০ অক্ষর

    text = (
        f"📨 **নতুন ইমেইল এসেছে!**\n\n"
        f"👤 **From:** {from_name} ({from_email})\n"
        f"📌 **Subject:** {subject}\n\n"
        f"📝 **Message:**\n{text_body}"
    )

    async with httpx.AsyncClient() as client:
        await client.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": telegram_id,
                "text": text,
                "parse_mode": "Markdown"
            }
        )

@router.post("/webhook/postmark")
async def postmark_webhook(request: Request):
    try:
        payload = await request.json()

        to_email = payload.get("Recipient") or payload.get("To")
        if not to_email:
            return {"status": "ignored", "reason": "no recipient"}

        # Clean email (Postmark sometimes sends with name)
        if "<" in to_email:
            to_email = to_email.split("<")[1].split(">")[0]
        to_email = to_email.strip().lower()

        user_email = await get_email_by_address(to_email)
        if not user_email:
            return {"status": "ignored", "reason": "email not registered"}

        # ইমেইল সেভ করো
        await save_incoming_email(user_email["id"], payload)

        # ★ ইউজারকে Telegram-এ নোটিফিকেশন পাঠাও
        user_response = supabase.table("users").select("telegram_id").eq("id", user_email["user_id"]).execute()
        if user_response.data:
            telegram_id = user_response.data[0]["telegram_id"]
            await send_telegram_notification(telegram_id, payload)

        print(f"📨 New email received for: {to_email}")
        return {"status": "success"}

    except Exception as e:
        print(f"Webhook Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
