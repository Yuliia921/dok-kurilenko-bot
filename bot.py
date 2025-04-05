
import logging
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import threading
import asyncio

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🧼 Минимальный бот запускается...")

# Хэндлер /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ /start получен")
    await update.message.reply_text("Бот работает! 🌸")

# Telegram бот
def run_telegram_bot():
    async def main():
        app = ApplicationBuilder().token("7591394007:AAHfjNZqLjdDDP0LpUfL7GvecfiZEgCAY_8").build()
        app.add_handler(CommandHandler("start", start))
        await app.bot.delete_webhook(drop_pending_updates=True)
        await app.start()
        await asyncio.Future()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

# Flask-заглушка
app = Flask(__name__)

@app.route("/")
def index():
    return "Док Куриленко бот 🌸"

if __name__ == "__main__":
    threading.Thread(target=run_telegram_bot).start()
    app.run(host="0.0.0.0", port=10000)
