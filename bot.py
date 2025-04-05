
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Хэндлер старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Осмотр', 'УЗИ', 'Консультация']]
    await update.message.reply_text(
        'Добро пожаловать в Док Куриленко 🌸\nВыберите шаблон:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

# Хэндлер сообщений (заглушка)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Протокол принят. Спасибо 🌸")

# Запуск бота
def run_telegram_bot():
    app = ApplicationBuilder().token("7591394007:AAHBZWhMJgpmnKY85suJaJ5AW_RpwPTZ9VI").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

# ---- Flask часть для Render ----
from flask import Flask
import threading

flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return 'Док Куриленко бот работает! 🌸'

if __name__ == '__main__':
    # Запускаем Telegram-бота в отдельном потоке
    threading.Thread(target=run_telegram_bot).start()
    # Запускаем Flask, чтобы Render не ругался
    flask_app.run(host='0.0.0.0', port=10000)
