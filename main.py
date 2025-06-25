from fastapi import FastAPI
from whatsapp.webhook import router as webhook_router

app = FastAPI()
app.include_router(webhook_router)
