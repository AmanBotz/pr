import os
import logging
from fastapi import FastAPI
import uvicorn
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from parmar_api import ParmarAPI
from video_processor import VideoProcessor
from utils import cleanup_user_data

# Initialize
app = Client("parmar_bot", 
             api_id=Config.API_ID,
             api_hash=Config.API_HASH,
             bot_token=Config.BOT_TOKEN)
api = ParmarAPI()
processor = VideoProcessor()

# States
STATE = {}

@app.on_message(filters.command("start"))
async def start(client, message):
    # Implement full conversation handler
    pass

@app.on_callback_query()
async def handle_callbacks(client, query):
    # Implement callback handlers
    pass

@app.on_message(filters.command("test50"))
async def test_command(client, message):
    # Implement test logic
    pass

if __name__ == "__main__":
    app.run()

# Add at bottom of file
web_app = FastAPI()

@web_app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(web_app, host="0.0.0.0", port=8000)
