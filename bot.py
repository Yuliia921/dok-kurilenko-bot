
import logging
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🔁 Бот запускается через run_polling...")

# Хэндлеры
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("✅ Получена команда /start")
    await update.message.reply_text("Док Куриленко 🌸 на связи! Новый бот, новый стиль!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"📩 Сообщение от пользователя: {update.message.text}")
    await update.message.reply_text("Принято 🌸")

# Flask-заглушка
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "Док Куриленко 🌸 Бот работает (polling)"

# Telegram бот (запускается в потоке)
def run_bot():
    async def main():
        app = ApplicationBuilder().token("7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU").build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        logger.info("🚀 Запуск polling...")
        await app.run_polling()

    asyncio.run(main())

if __name__ == "__main__":
    import threading
    threading.Thread(target=run_bot).start()
    flask_app.run(host="0.0.0.0", port=10000)
