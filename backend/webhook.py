from fastapi import APIRouter, Request, HTTPException
from backend.database import supabase
from backend.crud import get_email_by_address, save_incoming_email
import json

router = APIRouter()

@router.post("/webhook/postmark")
async def postmark_webhook(request: Request):
    try:
        payload = await request.json()
        
        # Recipient email address
        to_email = payload.get("Recipient") or payload.get("To")
        if not to_email:
            return {"status": "ignored", "reason": "no recipient"}

        # খুঁজে বের করো কোন ইউজারের ইমেইল
        user_email = await get_email_by_address(to_email)
        if not user_email:
            return {"status": "ignored", "reason": "email not registered"}

        # ইমেইল সেভ করো
        await save_incoming_email(user_email["id"], payload)

        print(f"📨 New email received for: {to_email}")
        
        return {"status": "success"}
        
    except Exception as e:
        print(f"Webhook Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
