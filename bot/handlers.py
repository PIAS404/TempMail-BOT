from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from bot.keyboards import main_menu, cancel_keyboard
from backend.crud import get_or_create_user, create_user_email, get_user_emails
from backend.config import DOMAIN
import random
import string

router = Router()

def generate_random_email():
    rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{rand_str}@{DOMAIN}"


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "👋 **স্বাগতম TempMail BOT-এ!**\n\n"
        f"তোমার ডোমেইন: `{DOMAIN}`\n\n"
        "নিচের মেনু থেকে অপশন বেছে নাও 👇",
        reply_markup=main_menu()
    )


@router.message(F.text == "📧 Random Email")
async def random_email_handler(message: Message):
    email = generate_random_email()
    
    await create_user_email(message.from_user.id, email)
    
    await message.answer(
        f"✅ **র‍্যান্ডম ইমেইল তৈরি হয়েছে!**\n\n"
        f"`{email}`\n\n"
        "এই ঠিকানায় যেকোনো মেইল পাঠালে সাথে সাথে নোটিফিকেশন পাবে।",
        reply_markup=main_menu()
    )


@router.message(F.text == "✍️ Custom Email")
async def ask_custom_email(message: Message):
    await message.answer(
        "✍️ তোমার পছন্দের ইমেইল প্রিফিক্স লিখো:\n\n"
        "উদাহরণ: `rakib`, `business2025`, `john123`\n\n"
        "শুধু প্রিফিক্স লিখো:",
        reply_markup=cancel_keyboard()
    )


@router.message(F.text == "🔙 Cancel")
async def cancel_handler(message: Message):
    await message.answer("❌ কাস্টম ইমেইল বাতিল করা হয়েছে।", reply_markup=main_menu())


@router.message(F.text == "📬 My Emails")
async def my_emails_handler(message: Message):
    emails = await get_user_emails(message.from_user.id)
    
    if not emails:
        await message.answer("এখনো কোনো ইমেইল তৈরি করোনি।", reply_markup=main_menu())
        return
    
    text = "📬 **তোমার ইমেইলগুলো:**\n\n"
    for e in emails:
        text += f"• `{e['email_address']}`\n"
    
    await message.answer(text, reply_markup=main_menu())


@router.message(F.text == "📥 Inbox")
async def inbox_handler(message: Message):
    await message.answer("📥 **Inbox শীঘ্রই আসছে...**", reply_markup=main_menu())


@router.message(F.text == "⭐ Help")
async def help_handler(message: Message):
    await message.answer(
        "🛠 **সাহায্য**\n\n"
        "• Random Email → অটো জেনারেট\n"
        "• Custom Email → নিজে নাম দাও\n"
        "• My Emails → তোমার সব ইমেইল দেখো\n\n"
        "সমস্যা হলে জানাও।",
        reply_markup=main_menu()
    )
