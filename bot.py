
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging
from flask import Flask

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

# Telegram-бот как async-задача
async def telegram_task():
    app = ApplicationBuilder().token("7591394007:AAHBZWhMJgpmnKY85suJaJ5AW_RpwPTZ9VI").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.initialize()
    await app.start()
    await app.bot.set_my_commands([("start", "Запустить бота")])
    await app.updater.start_polling()
    await app.updater.idle()

# Flask-приложение как async-задача
async def flask_task():
    flask_app = Flask(__name__)

    @flask_app.route('/')
    def index():
        return 'Док Куриленко бот работает! 🌸'

    from werkzeug.serving import run_simple
    run_simple("0.0.0.0", 10000, flask_app, use_reloader=False)

# Главный запуск: запускаем оба async-задачи
async def main():
    await asyncio.gather(
        telegram_task(),
        flask_task()
    )

if __name__ == '__main__':
    asyncio.run(main())
