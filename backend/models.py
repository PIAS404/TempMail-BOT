from datetime import datetime
from typing import Optional

# Supabase-এর জন্য টেবিল স্ট্রাকচার (Pydantic Models)

class User:
    """ইউজারের তথ্য"""
    id: Optional[int] = None
    telegram_id: int
    created_at: Optional[datetime] = None


class UserEmail:
    """একজন ইউজারের একাধিক ইমেইল সাপোর্ট করার জন্য"""
    id: Optional[int] = None
    user_id: int
    email_address: str
    created_at: Optional[datetime] = None


class Email:
    """যে মেইলগুলো আসবে সেগুলোর তথ্য"""
    id: Optional[int] = None
    user_email_id: int          # কোন ইমেইল অ্যাড্রেসে এসেছে
    from_email: str
    from_name: Optional[str] = None
    subject: str
    text_body: Optional[str] = None
    html_body: Optional[str] = None
    message_id: Optional[str] = None
    received_at: Optional[datetime] = None
