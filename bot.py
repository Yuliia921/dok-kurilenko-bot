
import os
import json
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
from generate_pdf import generate_pdf

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_state = {}

with open("templates.json", "r", encoding="utf-8") as f:
    templates = json.load(f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[name] for name in templates] + [["🛑 Стоп"]]
    await update.message.reply_text("Выберите шаблон:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_state:
        del user_state[user_id]
    await update.message.reply_text("⛔️ Ввод остановлен.", reply_markup=ReplyKeyboardRemove())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "🛑 Стоп":
        await stop(update, context)
        return

    if user_id not in user_state:
        if text in templates:
            user_state[user_id] = {
                "template": text,
                "fields": templates[text],
                "data": {},
                "current_field": 0,
            }
            await update.message.reply_text(f"Введите {templates[text][0]}:")
        else:
            await update.message.reply_text("Пожалуйста, выберите шаблон из меню.")
    else:
        state = user_state[user_id]
        field = state["fields"][state["current_field"]]
        state["data"][field] = text
        state["current_field"] += 1

        if state["current_field"] < len(state["fields"]):
            next_field = state["fields"][state["current_field"]]
            await update.message.reply_text(f"Введите {next_field}:")
        else:
            filepath = generate_pdf(state["template"], state["data"])
            await update.message.reply_document(document=open(filepath, "rb"))
            del user_state[user_id]

def main():
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
