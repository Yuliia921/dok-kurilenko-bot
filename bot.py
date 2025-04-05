
import asyncio
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
from werkzeug.serving import run_simple

# Логи
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🔧 Старт скрипта bot.py")

# Telegram хэндлеры
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Осмотр', 'УЗИ', 'Консультация']]
    await update.message.reply_text(
        'Добро пожаловать в Док Куриленко 🌸\nВыберите шаблон:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Протокол принят. Спасибо 🌸")

# Telegram-бот запуск
async def telegram_task():
    logger.info("🚀 Telegram-бот запускается...")
    app = ApplicationBuilder().token("7591394007:AAHBZWhMJgpmnKY85suJaJ5AW_RpwPTZ9VI").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.initialize()
    await app.start()
    await app.bot.set_my_commands([("start", "Запустить бота")])
    logger.info("✅ Telegram-бот запущен!")
    await app.updater.start_polling()
    await app.updater.idle()

# Flask-заглушка
def flask_task():
    logger.info("🌐 Flask запускается...")
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Док Куриленко бот работает! 🌸'

    run_simple("0.0.0.0", 10000, app, use_reloader=False)

# Комбинированный запуск
async def main():
    loop = asyncio.get_running_loop()
    flask_future = loop.run_in_executor(None, flask_task)
    telegram_future = telegram_task()
    await asyncio.gather(flask_future, telegram_future)

if __name__ == '__main__':
    asyncio.run(main())
