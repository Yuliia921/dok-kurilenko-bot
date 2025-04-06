import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask
import threading

# 🔧 Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🔧 Старт bot.py")

# 🔘 Flask-заглушка
flask_app = Flask(__name__)
@flask_app.route("/")
def index():
    return "Док Куриленко бот работает! 🌸"

def run_flask():
    flask_app.run(host="0.0.0.0", port=10000)

# 🤖 Хендлеры
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Осмотр", "УЗИ", "Консультация"]]
    await update.message.reply_text(
        "Добро пожаловать в Док Куриленко 🌸\nВыберите шаблон:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Протокол принят. Спасибо 🌸")

# 🚀 Запуск Telegram-бота
async def run_bot():
    app = ApplicationBuilder().token("7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("✅ Бот запущен")
    await app.run_polling()

if __name__ == "__main__":
    # 🔄 Flask в фоне
    threading.Thread(target=run_flask).start()
    # 🚀 Telegram-бот в основном потоке
    import asyncio
    asyncio.run(run_bot())