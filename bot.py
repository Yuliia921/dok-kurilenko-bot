
import logging
import threading
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)
import asyncio

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🔧 Старт bot.py")

# Логирование всех апдейтов
async def log_all_updates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 Update received:")
    print(update)

# Хэндлер /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ Handler 'start' triggered")
    reply_keyboard = [['Осмотр', 'УЗИ', 'Консультация']]
    await update.message.reply_text(
        'Добро пожаловать в Док Куриленко 🌸\nВыберите шаблон:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

# Хэндлер обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✉️ Handler 'handle_message' triggered")
    await update.message.reply_text("Протокол принят. Спасибо 🌸")

# Запуск Telegram-бота
def run_telegram_bot():
    logger.info("🚀 Telegram-бот запускается...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = ApplicationBuilder().token("7591394007:AAHBZWhMJgpmnKY85suJaJ5AW_RpwPTZ9VI").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.ALL, log_all_updates))  # Логирование всего

    async def run():
        await app.initialize()
        await app.bot.delete_webhook(drop_pending_updates=True)
        await app.start()
        await app.bot.set_my_commands([("start", "Запустить бота")])
        logger.info("✅ Telegram-бот запущен!")
        await asyncio.Future()

    loop.run_until_complete(run())

# Flask-заглушка
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return 'Док Куриленко бот работает! 🌸'

if __name__ == '__main__':
    threading.Thread(target=run_telegram_bot).start()
    flask_app.run(host='0.0.0.0', port=10000)
