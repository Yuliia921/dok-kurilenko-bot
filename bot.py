
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask
import threading
import asyncio
import os
from reportlab.pdfgen import canvas

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🔧 Старт bot.py")

flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return 'Док Куриленко бот работает! 🌸'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Консультативное заключение']]
    await update.message.reply_text(
        "Добро пожаловать в Док Куриленко 🌸\nВыберите шаблон:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Консультативное заключение":
        await update.message.reply_text("Пожалуйста, введите данные заключения в формате:\nФИО; Возраст; Диагноз; Обследование; Рекомендации")
    elif ";" in text:
        try:
            fio, age, diagnosis, exam, rec = [x.strip() for x in text.split(";")]
            file_path = f"/tmp/{fio.replace(' ', '_')}_zakl.pdf"
            c = canvas.Canvas(file_path)
            c.drawString(100, 800, f"ФИО: {fio}")
            c.drawString(100, 780, f"Возраст: {age}")
            c.drawString(100, 760, f"Диагноз: {diagnosis}")
            c.drawString(100, 740, f"Обследование: {exam}")
            c.drawString(100, 720, f"Рекомендации: {rec}")
            c.drawString(100, 700, "Врач: Куриленко Ю.С.")
            c.save()
            await update.message.reply_document(document=open(file_path, "rb"), filename="zakluchenie.pdf")
        except Exception as e:
            await update.message.reply_text("Ошибка при обработке заключения. Проверьте формат.")
            logger.error(f"❌ Ошибка при генерации PDF: {e}")
    else:
        await update.message.reply_text("Команда не распознана. Выберите шаблон или следуйте инструкциям.")

def run_bot():
    async def main():
        app = ApplicationBuilder().token(os.environ.get("BOT_TOKEN")).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        await app.updater.idle()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    flask_app.run(host='0.0.0.0', port=10000)
