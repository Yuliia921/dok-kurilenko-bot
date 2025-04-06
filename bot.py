import os
import logging
import asyncio
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🔧 Старт bot.py")

# Flask-заглушка
web_app = Flask(__name__)

@web_app.route('/')
def index():
    return "Док Куриленко бот работает! 🌸"

# Telegram хэндлеры
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Осмотр', 'УЗИ', 'Консультация']]
    await update.message.reply_text(
        "Добро пожаловать в Док Куриленко 🌸\nВыберите шаблон:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Протокол принят. Спасибо 🌸")

# Основной запуск
async def run_bot():
    app = ApplicationBuilder().token("7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    await app.bot.delete_webhook(drop_pending_updates=True)
    logger.info("✅ Бот запущен")
    await app.run_polling()

if __name__ == '__main__':
    # Запуск Flask и Telegram параллельно
    def start():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_bot())

    import threading
    threading.Thread(target=start).start()

    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)