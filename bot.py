
import logging
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import threading
import asyncio
from telegram.request import HTTPXRequest

# Логи
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🔧 Запуск нового бота с новым токеном и логами...")

# Хэндлер /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("✅ Получена команда /start")
    await update.message.reply_text("Бот с новым токеном жив! 🌸")

# Хэндлер на любое сообщение
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"📩 Получено сообщение: {update.message.text}")
    await update.message.reply_text("Сообщение получено 🌸")

# Telegram бот
def run_telegram_bot():
    async def main():
        request = HTTPXRequest(
            http_version="1.1",
            read_timeout=30,
            write_timeout=30,
            connect_timeout=30,
            pool_timeout=30
        )

        app = ApplicationBuilder().token("7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU").request(request).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.ALL, echo))

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
    return "Док Куриленко 🌸 Новый бот работает!"

if __name__ == "__main__":
    threading.Thread(target=run_telegram_bot).start()
    app.run(host="0.0.0.0", port=10000)
