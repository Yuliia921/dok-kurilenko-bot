import logging
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
from reportlab.pdfgen import canvas
from io import BytesIO
import asyncio
import threading

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🔧 Запуск Док Куриленко")

# Flask-заглушка
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return 'Док Куриленко бот работает! 🌸'

# Команды и обработчики
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['Консультативное заключение']]
    await update.message.reply_text(
        'Добро пожаловать в Док Куриленко 🌸\nВыберите шаблон:',
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'Консультативное заключение':
        await update.message.reply_text('Введите текст заключения:')
        return

    text = update.message.text
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 12)
    p.drawString(100, 800, "Консультативное заключение:")
    p.drawString(100, 780, text)
    p.drawString(100, 740, "Подпись: Куриленко Ю.С.")
    p.save()
    buffer.seek(0)
    await update.message.reply_document(document=buffer, filename="konsultaciya.pdf")
    logger.info(f"✅ PDF отправлен: {text}")

def run_bot():
    async def main():
        application = ApplicationBuilder().token("7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU").build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        await application.initialize()
        await application.start()
        await application.bot.set_my_commands([("start", "Запустить бота")])
        logger.info("✅ Бот запущен")
        await application.updater.start_polling()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    flask_app.run(host='0.0.0.0', port=10000)
