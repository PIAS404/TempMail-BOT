# backend/main.py

from fastapi import FastAPI
from backend.webhook import router as webhook_router

app = FastAPI(title="TempMail BOT Backend")

app.include_router(webhook_router)

@app.get("/")
async def root():
    return {"status": "✅ TempMail Backend is running!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
