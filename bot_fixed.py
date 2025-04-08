
import os
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from fastapi import FastAPI
from generate_pdf import generate_pdf

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_state = {}

templates = {
    "Консультативное заключение": ["ФИО", "Возраст", "Диагноз", "Обследование", "Рекомендации"],
    "УЗИ малого таза": [
        "ФИО", "Дата последней менструации", "Матка (положение, форма, размеры, структура миометрия)",
        "М-эхо", "Шейка матки", "Правый яичник", "Левый яичник", "Дополнительные образования",
        "Свободная жидкость", "Заключение", "Рекомендации"
    ],
}

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
            user_state[user_id] = {
                "template": text,
                "data": {},
                "fields": templates[text].copy()
            }
            current_field = user_state[user_id]["fields"].pop(0)
            await update.message.reply_text(f"Введите {current_field}:")
        else:
            await update.message.reply_text("Пожалуйста, выберите шаблон из меню.")
        return

    state = user_state[user_id]
    field = templates[state["template"]][len(state["data"])]
    state["data"][field] = text

    if state["fields"]:
        next_field = state["fields"].pop(0)
        await update.message.reply_text(f"Введите {next_field}:")
    else:
        filepath = generate_pdf(state["template"], state["data"])
        await update.message.reply_document(document=open(filepath, "rb"))
        del user_state[user_id]

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

fastapi_app = FastAPI()

@fastapi_app.get("/")
async def root():
    return {"status": "ok"}

@fastapi_app.on_event("startup")
async def on_startup():
    await app.bot.set_webhook(WEBHOOK_URL)

@fastapi_app.on_event("shutdown")
async def on_shutdown():
    await app.shutdown()

@fastapi_app.post("/webhook")
async def telegram_webhook(update: dict):
    await app.process_update(Update.de_json(update, app.bot))
    return {"ok": True}
