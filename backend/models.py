# backend/models.py

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[int] = None
    telegram_id: int
    created_at: Optional[datetime] = None

class UserEmail(BaseModel):
    id: Optional[int] = None
    user_id: int
    email_address: str
    created_at: Optional[datetime] = None

class Email(BaseModel):
    id: Optional[int] = None
    user_email_id: int
    from_email: str
    from_name: Optional[str] = None
    subject: str
    text_body: Optional[str] = None
    html_body: Optional[str] = None
    message_id: Optional[str] = None
    received_at: Optional[datetime] = None
