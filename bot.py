
import logging
from telegram import Update, ReplyKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

TOKEN = "7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_data = {}

# Регистрируем кириллический шрифт
pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Консультативное заключение"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Добро пожаловать в Док Куриленко 🌸\nВыберите шаблон:", reply_markup=reply_markup)

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

def generate_pdf(fields: dict) -> str:
    path = "consultation.pdf"
    c = canvas.Canvas(path)
    c.setFont("DejaVuSans", 12)
    c.drawString(100, 800, "Консультативное заключение")
    y = 770
    for k, v in fields.items():
        c.drawString(100, y, f"{k}: {v}")
        y -= 25
    c.drawString(100, y - 20, "Куриленко Ю.С.")
    c.save()
    return path

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
