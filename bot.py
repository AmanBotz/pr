import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from parmar_api import ParmarAPI
import uvicorn

# Initialize FastAPI with lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logging.basicConfig(level=logging.INFO)
    await telegram_bot.start()
    logging.info("Telegram bot started")
    yield
    # Shutdown
    await telegram_bot.stop()
    logging.info("Telegram bot stopped")

app = FastAPI(lifespan=lifespan)
api = ParmarAPI()

# Create Pyrogram client
telegram_bot = Client(
    "parmar_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# FastAPI Health Check
@app.get("/")
async def health_check():
    return {"status": "ok"}

# Telegram Handlers
@telegram_bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Welcome! Send /courses to begin")

@telegram_bot.on_message(filters.command("courses"))
async def show_courses(client, message):
    courses = await api.get_courses()
    buttons = [[InlineKeyboardButton(
        course["course_name"], 
        callback_data=f"course_{course['id']}"
    )] for course in courses]
    await message.reply(
        "Select a course:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@telegram_bot.on_callback_query(filters.regex(r"^course_"))
async def handle_course(client, callback):
    course_id = callback.data.split("_")[1]
    await callback.answer()
    await callback.edit_message_text(f"Selected Course ID: {course_id}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
