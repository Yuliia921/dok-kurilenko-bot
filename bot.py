import os
import logging
import telegram
import fpdf
print(">>> fpdf version:", fpdf.__version__)
from io import BytesIO
from telegram.error import Conflict
from telegram import Update, ReplyKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from generate_pdf import generate_pdf

TOKEN = "7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU"

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
                file_size = os.path.getsize(filepath)
                logger.info(f"📄 PDF создан: {filepath}, размер: {file_size} байт")
                await update.message.reply_document(
                    document=BytesIO(open(filepath, 'rb').read()), filename=os.path.basename(filepath),
                    caption="Консультативное заключение 🌸"
                )
                del user_data[chat_id]
        else:
            await update.message.reply_text("Шаблон завершён.")
    else:
        await update.message.reply_text("Пожалуйста, начните с команды /start")

if __name__ == "__main__":
    try:
        telegram.Bot(token=TOKEN).delete_webhook(drop_pending_updates=True)
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app.run_polling()
    except Conflict as e:
        logger.error("❌ Конфликт: бот уже работает где-то ещё. Завершение.")
    except Exception as e:
        logger.exception(f"❌ Ошибка при запуске: {e}")