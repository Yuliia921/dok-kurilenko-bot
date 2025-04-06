
import logging
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import threading
import asyncio
import httpx
from telegram.request import HTTPXRequest

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🛠️ Бот с таймаутами и инициализацией запускается...")

# Хэндлер /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ /start получен")
    await update.message.reply_text("Бот работает с таймаутами и инициализацией! 🌸")

# Telegram бот
def run_telegram_bot():
    async def main():
        # HTTP-клиент с таймаутом
        httpx_client = httpx.AsyncClient(timeout=30)
        request = HTTPXRequest(http_version="1.1", client=httpx_client)

        app = ApplicationBuilder().token("7591394007:AAHfjNZqLjdDDP0LpUfL7GvecfiZEgCAY_8").request(request).build()
        app.add_handler(CommandHandler("start", start))
        await app.bot.delete_webhook(drop_pending_updates=True)
        await app.initialize()
        await app.start()
        await asyncio.Future()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")

# Flask-заглушка
app = Flask(__name__)

@app.route("/")
def index():
    return "Док Куриленко бот 🌸 (с таймаутами и initialize)"

if __name__ == "__main__":
    threading.Thread(target=run_telegram_bot).start()
    app.run(host="0.0.0.0", port=10000)
