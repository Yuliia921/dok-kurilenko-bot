import logging
import asyncio
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🔧 Бот запускается...")

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Консультативное заключение']]
    await update.message.reply_text(
        "Добро пожаловать в Док Куриленко 🌸
Выберите шаблон:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

# Функция запуска Telegram-бота
async def run_bot():
    app = ApplicationBuilder().token("7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU").build()
    app.add_handler(CommandHandler("start", start))

    logger.info("✅ Telegram-бот запущен и готов к работе")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

# Flask-заглушка для Render
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return 'Док Куриленко бот работает! 🌸'

# Запуск Flask и Telegram
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(run_bot())
    flask_app.run(host='0.0.0.0', port=10000)