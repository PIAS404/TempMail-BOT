import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

load_dotenv()

from bot.handlers import router

# Bot Setup
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found in .env file")

bot = Bot(token=TELEGRAM_TOKEN, parse_mode="Markdown")
dp = Dispatcher()

# Include all handlers
dp.include_router(router)

async def main():
    logging.basicConfig(level=logging.INFO)
    print("🤖 TempMail Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
