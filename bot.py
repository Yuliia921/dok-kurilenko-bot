import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputFile
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from generate_pdf import generate_pdf
from templates import templates

BOT_TOKEN = os.getenv("BOT_TOKEN")

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[k] for k in templates] + [["🛑 Стоп"]]
    await update.message.reply_text("Выберите шаблон:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_state:
        del user_state[user_id]
        await update.message.reply_text("⛔️ Ввод прерван. Вы можете начать заново с /start", reply_markup=ReplyKeyboardRemove())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "🛑 Стоп":
        await stop(update, context)
        return

    if user_id not in user_state:
        if text in templates:
            user_state[user_id] = {"template": text, "data": {}, "step": 0}
            field = templates[text]["fields"][0]
            await update.message.reply_text(f"Введите {field}:")
        else:
            await update.message.reply_text("Пожалуйста, выберите шаблон из меню.")
        return

    state = user_state[user_id]
    fields = templates[state["template"]]["fields"]
    if state["step"] < len(fields):
        state["data"][fields[state["step"]]] = text
        state["step"] += 1

    if state["step"] == len(fields):
        filepath = generate_pdf(state["template"], state["data"])
        await update.message.reply_document(document=InputFile(filepath), filename=os.path.basename(filepath))
        del user_state[user_id]
    else:
        next_field = fields[state["step"]]
        await update.message.reply_text(f"Введите {next_field}:")

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
