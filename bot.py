
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Этапы диалога
COMPLAINTS, ANAMNESIS, EXAM = range(3)

user_data_storage = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['Осмотр']]
    await update.message.reply_text(
        "Добро пожаловать в Док Куриленко 🌸\nВыберите шаблон:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )
    logger.info(f"👤 /start от {update.effective_user.first_name}")

async def start_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔹 Шаблон 'Осмотр' выбран. Введите жалобы пациента:")
    return COMPLAINTS

async def receive_complaints(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["Жалобы"] = update.message.text
    await update.message.reply_text("🩺 Введите анамнез заболевания:")
    return ANAMNESIS

async def receive_anamnesis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["Анамнез"] = update.message.text
    await update.message.reply_text("🔍 Опишите объективный статус:")
    return EXAM

async def receive_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["Объективно"] = update.message.text

    summary = "\n".join([f"{k}: {v}" for k, v in context.user_data.items()])
    await update.message.reply_text(f"🌸 Протокол 'Осмотр':\n{summary}")
    logger.info(f"✅ Протокол сформирован для {update.effective_user.first_name}:\n{summary}")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Ввод отменён.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token("7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU").build()

    exam_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^(Осмотр)$"), start_exam)],
        states={
            COMPLAINTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_complaints)],
            ANAMNESIS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_anamnesis)],
            EXAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_exam)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(exam_conv)
    app.run_polling()

if __name__ == "__main__":
    main()
