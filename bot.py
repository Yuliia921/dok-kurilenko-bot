
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from generate_pdf import generate_pdf
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

templates = {
    "📝 Консультация": [
        "ФИО", "Возраст", "Жалобы", "Анамнез", "Диагноз", "Рекомендации"
    ],
    "🧭 УЗИ": [
        "ФИО", "Дата последней менструации", "Положение матки", "Размеры матки", "Структура миометрия",
        "М-эхо", "Состояние шейки", "Размеры и структура яичников", "Наличие образований", "Свободная жидкость",
        "Заключение", "Рекомендации"
    ]
}

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[k] for k in templates] + [["🛑 Стоп"]]
    await update.message.reply_text(
        "Выберите шаблон:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )

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
            user_state[user_id] = {"template": text, "step": 0, "data": {}}
            await update.message.reply_text(f"{templates[text][0]}:")
        else:
            await update.message.reply_text("Пожалуйста, выберите шаблон из меню.")
    else:
        state = user_state[user_id]
        field = templates[state["template"]][state["step"]]
        state["data"][field] = text
        state["step"] += 1

        if state["step"] < len(templates[state["template"]]):
            next_field = templates[state["template"]][state["step"]]
            await update.message.reply_text(f"{next_field}:")
        else:
            filepath = generate_pdf(state["template"], state["data"])
            await update.message.reply_document(
                document=InputFile(filepath, filename=os.path.basename(filepath))
            )
            del user_state[user_id]

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

import asyncio
from fastapi import FastAPI
from telegram.ext import Application

fastapi_app = FastAPI()

@fastapi_app.on_event("startup")
async def on_startup():
    await app.bot.set_webhook(WEBHOOK_URL)

@fastapi_app.post(f"/{BOT_TOKEN}")
async def telegram_webhook(update: dict):
    await app.update_queue.put(Update.de_json(update, app.bot))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("bot:fastapi_app", host="0.0.0.0", port=10000)
