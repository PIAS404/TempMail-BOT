# bot/keyboards.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📧 Random Email"), KeyboardButton(text="✍️ Custom Email")],
            [KeyboardButton(text="📬 My Emails"), KeyboardButton(text="📥 Inbox")],
            [KeyboardButton(text="⭐ Help")]
        ],
        resize_keyboard=True
    )
    return keyboard

def cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔙 Cancel")]
        ],
        resize_keyboard=True
    )
    return keyboard
