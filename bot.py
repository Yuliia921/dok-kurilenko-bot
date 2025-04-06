from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging
from flask import Flask
import threading

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask-заглушка
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return "🌸 Док Куриленко бот активен!"

# Хэндлер /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот работает ✅")

# Основной запуск
def run_telegram_bot():
    logger.info("🚀 Старт бота...")
    app = ApplicationBuilder().token("7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU").build()
    app.add_handler(CommandHandler("start", start))

    async def run():
        await app.initialize()
        await app.start()
        await app.bot.delete_webhook()
        logger.info("✅ Бот запущен")
        await app.updater.start_polling()
        await app.updater.idle()

    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())

if __name__ == '__main__':
    threading.Thread(target=run_telegram_bot).start()
    flask_app.run(host='0.0.0.0', port=10000)

