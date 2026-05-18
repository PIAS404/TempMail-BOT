from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    """মেইন মেনু কীবোর্ড"""
    keyboard = [
        [KeyboardButton(text="📧 Random Email"), KeyboardButton(text="✍️ Custom Email")],
        [KeyboardButton(text="📬 My Emails"), KeyboardButton(text="📥 Inbox")],
        [KeyboardButton(text="⭐ Help")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, persistent=True)


def cancel_keyboard():
    """কাস্টম ইমেইলের সময় ব্যাক করার জন্য"""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Cancel")]],
        resize_keyboard=True
    )
