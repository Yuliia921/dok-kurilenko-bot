
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, BotCommand
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters, ConversationHandler
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NAME, COMPLAINTS, ANAMNESIS, EXAM = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("Осмотр")], [KeyboardButton("Просмотр протокола")]]
    await update.message.reply_text(
        "Добро пожаловать в Док Куриленко 🌸\nВыберите действие:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    logger.info(f"👤 /start от {update.effective_user.first_name}")

async def start_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("📝 Введите ФИО пациента:")
    return NAME

async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ФИО"] = update.message.text
    await update.message.reply_text("🔹 Введите жалобы пациента:")
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
    logger.info(f"✅ Протокол сформирован: {summary}")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Ввод отменён.")
    return ConversationHandler.END

async def show_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data:
        summary = "\n".join([f"{k}: {v}" for k, v in context.user_data.items()])
        await update.message.reply_text(f"📄 Текущий протокол:\n{summary}")
    else:
        await update.message.reply_text("⚠️ Протокол пуст. Сначала заполните шаблон 'Осмотр'.")

def main():
    app = ApplicationBuilder().token("7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CommandHandler("summary", show_summary))
    app.add_handler(MessageHandler(filters.Regex("^(Просмотр протокола)$"), show_summary))

    exam_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^(Осмотр)$"), start_exam)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)],
            COMPLAINTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_complaints)],
            ANAMNESIS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_anamnesis)],
            EXAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_exam)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(exam_conv)

    async def set_commands(_: ContextTypes.DEFAULT_TYPE):
        await app.bot.set_my_commands([
            BotCommand("start", "Запустить бота"),
            BotCommand("cancel", "Отменить ввод"),
            BotCommand("summary", "Просмотреть текущий протокол"),
        ])

    app.post_init = set_commands
    app.run_polling()

if __name__ == "__main__":
    main()
