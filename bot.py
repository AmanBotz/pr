import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fastapi import FastAPI
import uvicorn
import threading
from config import Config
from parmar_api import ParmarAPI

# Initialize
app = FastAPI()
telegram_bot = Client(
    "parmar_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)
api = ParmarAPI()

# FastAPI Endpoint for Health Check
@app.get("/")
def health_check():
    return {"status": "running"}

# Telegram Bot Handlers
@telegram_bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Welcome to Parmar Academy Bot! Send /courses to begin")

@telegram_bot.on_message(filters.command("courses"))
async def show_courses(client, message):
    courses = await api.get_courses()
    keyboard = []
    for course in courses:
        keyboard.append([InlineKeyboardButton(
            course["course_name"],
            callback_data=f"course_{course['id']}"
        )])
    await message.reply(
        "Select a course:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Callback Handlers
@telegram_bot.on_callback_query()
async def handle_callback(client, callback_query):
    data = callback_query.data
    if data.startswith("course_"):
        course_id = data.split("_")[1]
        subjects = await api.get_subjects(course_id)
        # Add subject selection logic
        await callback_query.answer()
        await callback_query.edit_message_text("Feature not fully implemented yet")

# Startup Event
@app.on_event("startup")
async def startup():
    await telegram_bot.start()
    logging.info("Telegram bot started")

# Shutdown Event
@app.on_event("shutdown")
async def shutdown():
    await telegram_bot.stop()
    logging.info("Telegram bot stopped")

# Run both services
def run_bot():
    telegram_bot.run()

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
