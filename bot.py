
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging
from flask import Flask
import threading

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Хэндлер /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Осмотр', 'УЗИ', 'Консультация']]
    await update.message.reply_text(
        'Добро пожаловать в Док Куриленко 🌸\nВыберите шаблон:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

# Хэндлер текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Протокол принят. Спасибо 🌸")

# Функция запуска бота (async)
async def run_telegram_bot():
    app = ApplicationBuilder().token("7591394007:AAHBZWhMJgpmnKY85suJaJ5AW_RpwPTZ9VI").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

# Flask-заглушка для Render
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return 'Док Куриленко бот работает! 🌸'

# Одновременный запуск Flask и Telegram-бота
def start_all():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_telegram_bot())

if __name__ == '__main__':
    threading.Thread(target=start_all).start()
    flask_app.run(host='0.0.0.0', port=10000)
