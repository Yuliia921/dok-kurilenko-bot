import logging
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🔧 Запуск нового бота с новым токеном и логами...")

app = Flask(__name__)

@app.route('/')
def index():
    return "Док Куриленко бот работает 🌸"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Осмотр', 'УЗИ', 'Консультация']]
    await update.message.reply_text(
        "Добро пожаловать в Док Куриленко 🌸
Выберите шаблон:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Протокол принят. Спасибо 🌸")

def run_bot():
    async def main():
        application = ApplicationBuilder().token("7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU").build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        await application.initialize()
        await application.start()
        logger.info("✅ Бот запущен")
        await application.updater.start_polling()
        await application.updater.wait()

    asyncio.run(main())

if __name__ == '__main__':
    from threading import Thread
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)