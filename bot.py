import asyncio
import logging
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask-заглушка
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "Док Куриленко бот работает! 🌸"

# Хэндлеры
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["Осмотр", "УЗИ", "Консультация"]]
    await update.message.reply_text(
        "Добро пожаловать в Док Куриленко 🌸\nВыберите шаблон:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Протокол принят. Спасибо 🌸")

# Асинхронная инициализация бота
async def main():
    application = ApplicationBuilder().token("7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.initialize()
    await application.start()
    logger.info("✅ Бот запущен")
    await application.updater.start_polling()
    await application.updater.wait()

if __name__ == "__main__":
    import threading

    # Flask в отдельном потоке
    threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=10000)).start()
    asyncio.run(main())
