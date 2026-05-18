# bot/handlers.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards import main_menu, cancel_keyboard
from backend.crud import get_or_create_user, create_user_email, get_user_emails, get_inbox_for_user, get_email_by_address
from backend.config import DOMAIN
import re
import random
import string

router = Router()

# FSM States
class EmailStates(StatesGroup):
    waiting_for_prefix = State()

def generate_random_email():
    rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{rand_str}@{DOMAIN}"

@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await get_or_create_user(message.from_user.id)
    await message.answer(
        f"👋 **স্বাগতম TempMail BOT-এ!**\n\n"
        f"তোমার ডোমেইন: `{DOMAIN}`\n\n"
        "নিচের মেনু থেকে অপশন বেছে নাও 👇",
        reply_markup=main_menu()
    )

@router.message(F.text == "📧 Random Email")
async def random_email_handler(message: Message, state: FSMContext):
    await state.clear()
    email = generate_random_email()
    await create_user_email(message.from_user.id, email)
    await message.answer(
        f"✅ **র‍্যান্ডম ইমেইল তৈরি হয়েছে!**\n\n"
        f"`{email}`\n\n"
        "এই ঠিকানায় যেকোনো মেইল পাঠালে সাথে সাথে নোটিফিকেশন পাবে।",
        reply_markup=main_menu()
    )

@router.message(F.text == "✍️ Custom Email")
async def ask_custom_email(message: Message, state: FSMContext):
    await state.set_state(EmailStates.waiting_for_prefix)
    await message.answer(
        "✍️ তোমার পছন্দের ইমেইল প্রিফিক্স লিখো:\n\n"
        f"উদাহরণ: `rakib` → rakib@{DOMAIN}\n"
        f"অথবা পুরো লিখো: `rakib@{DOMAIN}`\n\n"
        "লিখো:",
        reply_markup=cancel_keyboard()
    )

@router.message(F.text == "🔙 Cancel")
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ বাতিল করা হয়েছে।", reply_markup=main_menu())

@router.message(EmailStates.waiting_for_prefix)
async def process_custom_email(message: Message, state: FSMContext):
    text = message.text.strip().lower()

    # যদি পুরো ইমেইল লিখে (help@piasx.top) তাহলে prefix বের করো
    if "@" in text:
        prefix = text.split("@")[0]
    else:
        prefix = text

    # Validate prefix
    if len(prefix) < 1 or len(prefix) > 30:
        await message.answer(
            "❌ প্রিফিক্স ১ থেকে ৩০ অক্ষরের মধ্যে হতে হবে।\n"
            "আবার চেষ্টা করো:",
            reply_markup=cancel_keyboard()
        )
        return

    if not re.match(r'^[a-z0-9][a-z0-9._-]*$', prefix):
        await message.answer(
            "❌ অবৈধ প্রিফিক্স!\n\n"
            "শুধু ইংরেজি ছোট হাতের অক্ষর, সংখ্যা, dot, hyphen ব্যবহার করো।\n"
            "প্রথম অক্ষর অবশ্যই letter বা number হতে হবে।\n"
            "আবার চেষ্টা করো:",
            reply_markup=cancel_keyboard()
        )
        return

    email = f"{prefix}@{DOMAIN}"

    existing = await get_email_by_address(email)
    if existing:
        await message.answer(
            f"⚠️ `{email}` আগে থেকেই নেওয়া আছে।\n"
            "অন্য প্রিফিক্স চেষ্টা করো:",
            reply_markup=cancel_keyboard()
        )
        return

    await create_user_email(message.from_user.id, email)
    await state.clear()
    await message.answer(
        f"✅ **কাস্টম ইমেইল তৈরি হয়েছে!**\n\n"
        f"`{email}`\n\n"
        "এই ঠিকানায় যেকোনো মেইল পাঠালে নোটিফিকেশন পাবে।",
        reply_markup=main_menu()
    )

@router.message(F.text == "📬 My Emails")
async def my_emails_handler(message: Message, state: FSMContext):
    await state.clear()
    emails = await get_user_emails(message.from_user.id)
    if not emails:
        await message.answer("এখনো কোনো ইমেইল তৈরি করোনি।", reply_markup=main_menu())
        return

    text = "📬 **তোমার ইমেইলগুলো:**\n\n"
    for e in emails:
        text += f"• `{e['email_address']}`\n"
    await message.answer(text, reply_markup=main_menu())

@router.message(F.text == "📥 Inbox")
async def inbox_handler(message: Message, state: FSMContext):
    await state.clear()
    emails = await get_user_emails(message.from_user.id)
    if not emails:
        await message.answer("আগে একটা ইমেইল তৈরি করো!", reply_markup=main_menu())
        return

    inbox = await get_inbox_for_user(message.from_user.id)
    if not inbox:
        await message.answer("📥 তোমার Inbox খালি। কোনো মেইল আসেনি এখনও।", reply_markup=main_menu())
        return

    text = "📥 **তোমার Inbox:**\n\n"
    for mail in inbox[:10]:
        text += (
            f"━━━━━━━━━━━━━━━\n"
            f"📨 **From:** {mail.get('from_name', 'Unknown')} ({mail.get('from_email', '')})\n"
            f"📌 **Subject:** {mail.get('subject', 'No Subject')}\n"
            f"🕐 {mail.get('received_at', '')}\n\n"
        )
    await message.answer(text, reply_markup=main_menu())

@router.message(F.text == "⭐ Help")
async def help_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🛠 **সাহায্য**\n\n"
        "• 📧 Random Email → অটো জেনারেট\n"
        "• ✍️ Custom Email → নিজে নাম দাও\n"
        "• 📬 My Emails → তোমার সব ইমেইল দেখো\n"
        "• 📥 Inbox → আসা মেইলগুলো দেখো\n\n"
        "সমস্যা হলে জানাও।",
        reply_markup=main_menu()
    )
