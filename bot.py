
import logging
import io
from telegram import Update, ReplyKeyboardMarkup, BotCommand, InputFile
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters
)
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FIO, AGE, DIAGNOSIS, EXAM, RECOMMENDATION = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        "Консультативное заключение"
    ]]
    await update.message.reply_text(
        "🌸 Док Куриленко. Выберите шаблон:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def start_consult(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["Дата"] = datetime.now().strftime("%d.%m.%Y")
    await update.message.reply_text("Введите ФИО пациента:")
    return FIO

async def receive_fio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ФИО"] = update.message.text
    await update.message.reply_text("Возраст:")
    return AGE

async def receive_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["Возраст"] = update.message.text
    await update.message.reply_text("Диагноз:")
    return DIAGNOSIS

async def receive_diagnosis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["Диагноз"] = update.message.text
    await update.message.reply_text("Обследование:")
    return EXAM

async def receive_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["Обследование"] = update.message.text
    await update.message.reply_text("Рекомендации:")
    return RECOMMENDATION

async def receive_recommendation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["Рекомендации"] = update.message.text
    await update.message.reply_text("📄 Генерирую PDF...")

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    p.setFont("Helvetica", 14)
    p.drawString(100, y, "🌸 Консультативное заключение")
    p.setFont("Helvetica", 11)
    y -= 30
    for key, value in context.user_data.items():
        p.drawString(50, y, f"{key}: {value}")
        y -= 20
    y -= 20
    p.drawString(50, y, "Подпись: Куриленко Ю.С.")

    p.showPage()
    p.save()
    buffer.seek(0)

    await update.message.reply_document(
        document=InputFile(buffer, filename="konsultaciya.pdf"),
        caption="Ваше консультативное заключение готово 🌸"
    )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Ввод отменён.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token("7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cancel", cancel))

    consult_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^(Консультативное заключение)$"), start_consult)],
        states={
            FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_fio)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_age)],
            DIAGNOSIS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_diagnosis)],
            EXAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_exam)],
            RECOMMENDATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_recommendation)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(consult_conv)

    async def set_commands(_: ContextTypes.DEFAULT_TYPE):
        await app.bot.set_my_commands([
            BotCommand("start", "Запустить бота"),
            BotCommand("cancel", "Отменить ввод")
        ])

    app.post_init = set_commands
    app.run_polling()

if __name__ == "__main__":
    main()
