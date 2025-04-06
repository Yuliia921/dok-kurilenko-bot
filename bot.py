import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask
import threading
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🔧 Старт bot.py")

# Хендлер старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Консультативное заключение']]
    await update.message.reply_text(
        "Добро пожаловать в Док Куриленко 🌸\nВыберите шаблон:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )

# Хендлер сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Консультативное заключение":
        await update.message.reply_text("Введите ФИО пациента:")
        context.user_data["state"] = "fio"
    elif context.user_data.get("state") == "fio":
        context.user_data["fio"] = update.message.text
        await update.message.reply_text("Введите возраст пациента:")
        context.user_data["state"] = "age"
    elif context.user_data.get("state") == "age":
        context.user_data["age"] = update.message.text
        await update.message.reply_text("Введите диагноз:")
        context.user_data["state"] = "diagnosis"
    elif context.user_data.get("state") == "diagnosis":
        context.user_data["diagnosis"] = update.message.text
        await update.message.reply_text("Введите обследование:")
        context.user_data["state"] = "exam"
    elif context.user_data.get("state") == "exam":
        context.user_data["exam"] = update.message.text
        await update.message.reply_text("Введите рекомендации:")
        context.user_data["state"] = "recommend"
    elif context.user_data.get("state") == "recommend":
        context.user_data["recommend"] = update.message.text
        fio = context.user_data.get("fio", "")
        age = context.user_data.get("age", "")
        diagnosis = context.user_data.get("diagnosis", "")
        exam = context.user_data.get("exam", "")
        recommend = context.user_data.get("recommend", "")
        text = f"🌸 Консультативное заключение 🌸\n\nФИО: {fio}\nВозраст: {age}\nДиагноз: {diagnosis}\nОбследование: {exam}\nРекомендации: {recommend}"
        await update.message.reply_text(text)
        context.user_data.clear()
    else:
        await update.message.reply_text("Пожалуйста, начните с выбора шаблона.")

# Telegram-бот
def run_bot():
    async def main():
        app = ApplicationBuilder().token("7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU").build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        logger.info("✅ Бот запущен")
        await app.run_polling()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

# Flask-заглушка
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "Док Куриленко бот работает! 🌸"

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    flask_app.run(host="0.0.0.0", port=10000)