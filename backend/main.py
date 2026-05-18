from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.webhook import router as webhook_router
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="TempMail Bot Backend",
    description="Webhook handler for Postmark inbound emails"
)

# CORS (optional but good practice)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include webhook routes
app.include_router(webhook_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "TempMail Bot Backend",
        "message": "Webhook is ready to receive emails from Postmark"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
