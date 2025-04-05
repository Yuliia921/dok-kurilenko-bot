
import logging
import threading
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🔧 Старт bot.py")

# Хэндлеры Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Осмотр', 'УЗИ', 'Консультация']]
    await update.message.reply_text(
        'Добро пожаловать в Док Куриленко 🌸\nВыберите шаблон:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Протокол принят. Спасибо 🌸")

# Telegram-бот (в отдельном потоке с event loop)
def run_telegram_bot():
    logger.info("🚀 Telegram-бот запускается...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = ApplicationBuilder().token("7591394007:AAHBZWhMJgpmnKY85suJaJ5AW_RpwPTZ9VI").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    async def run():
        await app.initialize()
        await app.start()
        await app.bot.set_my_commands([("start", "Запустить бота")])
        logger.info("✅ Telegram-бот запущен!")
        await app.idle()

    loop.run_until_complete(run())

# Flask-заглушка
app = Flask(__name__)

@app.route('/')
def index():
    return 'Док Куриленко бот работает! 🌸'

if __name__ == '__main__':
    threading.Thread(target=run_telegram_bot).start()
    app.run(host='0.0.0.0', port=10000)
