import os
import logging
from telegram import Update, ReplyKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from generate_pdf import generate_pdf

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Консультативное заключение"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Добро пожаловать в Док Куриленко 🌸\nВыберите шаблон:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.effective_chat.id

    if text == "Консультативное заключение":
        user_data[chat_id] = {"шаблон": "заключение", "поля": {}, "шаг": 0}
        await update.message.reply_text("Введите ФИО пациента:")
    elif chat_id in user_data:
        data = user_data[chat_id]
        шаг = data["шаг"]
        поля = ["ФИО", "Возраст", "Диагноз", "Обследование", "Рекомендации"]

        if шаг < len(поля):
            data["поля"][поля[шаг]] = text
            data["шаг"] += 1
            if data["шаг"] < len(поля):
                await update.message.reply_text(f"Введите {поля[data['шаг']]}:")
            else:
                filepath = generate_pdf(data["поля"])
                await update.message.reply_document(InputFile(filepath), caption="Консультативное заключение 🌸")
                del user_data[chat_id]
        else:
            await update.message.reply_text("Шаблон завершён.")
    else:
        await update.message.reply_text("Пожалуйста, начните с команды /start")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.initialize()
    await app.start()
    await app.bot.set_webhook(url=WEBHOOK_URL)
    await app.updater.start_polling()  # Просто чтобы держал активность
    await app.updater.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())