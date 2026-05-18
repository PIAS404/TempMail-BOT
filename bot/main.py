# bot/main.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.handlers import router

TELEGRAM_TOKEN = "8280327644:AAFEwkpyicJ4sbNHsahhXbJn5FnyRNqp19s"

bot = Bot(
    token=TELEGRAM_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
dp = Dispatcher()

dp.include_router(router)

async def main():
    logging.basicConfig(level=logging.INFO)
    print("🤖 TempMail Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
