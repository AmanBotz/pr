import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import uvicorn
from config import Config
from parmar_api import ParmarAPI

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Initialize services
api = ParmarAPI()
bot = Client(
    "parmar_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start Pyrogram bot
    await bot.start()
    logging.info("Bot started")
    yield
    # Stop Pyrogram bot
    await bot.stop()
    logging.info("Bot stopped")

app = FastAPI(lifespan=lifespan)

# Health check endpoint
@app.get("/")
async def health_check():
    return {"status": "running"}

# Telegram handlers
@bot.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply("🚀 Welcome to Parmar Academy Bot!\nSend /courses to begin")

@bot.on_message(filters.command("courses"))
async def courses_command(client, message):
    courses = await api.get_courses()
    buttons = [
        [InlineKeyboardButton(c["course_name"], f"course_{c['id']}")]
        for c in courses
    ]
    await message.reply(
        "📚 Available Courses:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@bot.on_callback_query(filters.regex(r"^course_"))
async def course_callback(client, callback):
    await callback.answer()
    course_id = callback.data.split("_")[1]
    await callback.edit_message_text(f"📖 Selected Course ID: {course_id}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
