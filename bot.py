
import logging
import os
import threading
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🔧 Запуск нового бота с PDF и логами...")

# Регистрация шрифта для кириллицы
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont("DejaVuSans", font_path))
else:
    logger.warning("⚠️ Шрифт DejaVuSans не найден. Кириллица в PDF может отображаться некорректно.")

# Хендлеры Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"📥 Команда /start от {update.effective_user.first_name}")
    reply_keyboard = [['Консультативное заключение']]
    await update.message.reply_text(
        'Добро пожаловать в Док Куриленко 🌸
Выберите шаблон:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"📩 Получено сообщение: {update.message.text} от {update.effective_user.first_name}")

    if update.message.text == "Консультативное заключение":
        filename = f"Consult_{update.effective_user.id}.pdf"
        c = canvas.Canvas(filename)
        if pdfmetrics.getRegisteredFontNames():
            c.setFont("DejaVuSans", 12)
        c.drawString(100, 750, f"Консультативное заключение для {update.effective_user.first_name}")
        c.drawString(100, 730, "Дата: __________")
        c.drawString(100, 710, "Диагноз: __________")
        c.drawString(100, 690, "Рекомендации: __________")
        c.save()

        logger.info(f"✅ PDF создан: {filename}")
        await update.message.reply_document(document=InputFile(filename), filename=filename)
        os.remove(filename)
    else:
        await update.message.reply_text("Протокол принят. Спасибо 🌸")

# Запуск Telegram-бота
def run_telegram_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = ApplicationBuilder().token("7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    async def main():
        await app.initialize()
        await app.start()
        await app.bot.delete_webhook()
        await app.set_my_commands([("start", "Запустить бота")])
        logger.info("✅ Telegram-бот запущен и готов к работе")
        await app.updater.start_polling()
        await app.updater.wait_until_closed()

    loop.run_until_complete(main())

# Flask-заглушка
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return 'Док Куриленко бот работает! 🌸'

# Запуск
if __name__ == '__main__':
    threading.Thread(target=run_telegram_bot).start()
    flask_app.run(host='0.0.0.0', port=10000)
