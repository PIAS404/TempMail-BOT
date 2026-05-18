# TempMail BOT

A Telegram bot that creates long-lived custom email addresses on your own domain and shows incoming emails directly inside Telegram.

## Features
- Random Email Generation
- Custom Email (user choice)
- Permanent Inbox (lifetime)
- Real-time email notification
- Built with Supabase + FastAPI + aiogram

## Tech Stack
- Python
- Supabase (PostgreSQL)
- FastAPI (Webhook)
- aiogram 3.x (Telegram Bot)
- Postmark (Inbound Email)

## Setup Instructions

1. Clone the repo
2. Copy `.env.example` to `.env`
3. Fill up all the credentials
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
