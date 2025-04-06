import logging
import asyncio
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🔧 Запуск Док Куриленко...")

# Хэндлер /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['Осмотр', 'УЗИ'], ['Консультация']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Добро пожаловать в Док Куриленко 🌸\nВыберите шаблон:",
        reply_markup=markup
    )

# Хэндлер текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(f"✅ Протокол '{update.message.text}' сформирован для {user}.")

# Основная функция запуска бота
async def main():
    app = ApplicationBuilder().token("7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.initialize()
    await app.start()
    await app.bot.delete_webhook()
    logger.info("✅ Бот запущен")

    await app.updater.start_polling()
    await app.updater.idle()

# Flask-заглушка
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return 'Док Куриленко работает! 🌸'

# Запуск Flask и Telegram параллельно
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(main())
    flask_app.run(host="0.0.0.0", port=10000)


