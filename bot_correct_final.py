
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputFile
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from fastapi import FastAPI
import asyncio
from generate_pdf import generate_pdf

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

fastapi_app = FastAPI()
app = ApplicationBuilder().token(BOT_TOKEN).build()

user_state = {}

templates = {
    "📝 Консультативное заключение": [
        "ФИО", "Возраст", "Диагноз", "Обследование", "Рекомендации"
    ],
    "🩺 УЗИ органов малого таза": [
        "ФИО", "Дата последней менструации", "Положение матки", "Размеры матки",
        "Структура миометрия", "М-эхо", "Состояние шейки матки", "Яичники",
        "Наличие образований", "Свободная жидкость", "Заключение", "Рекомендации"
    ]
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
    text = update.message.text.strip()

    if text == "🛑 Стоп":
        await stop(update, context)
        return

    if user_id not in user_state:
        if text in templates:
            user_state[user_id] = {"template": text, "fields": templates[text], "data": {}}
            first_field = user_state[user_id]["fields"][0]
            await update.message.reply_text(f"Введите значение для поля: {first_field}")
        else:
            await update.message.reply_text("Пожалуйста, выберите шаблон из меню или нажмите /start")
        return

    state = user_state[user_id]
    current_field_index = len(state["data"])

    if current_field_index < len(state["fields"]):
        field_name = state["fields"][current_field_index]
        if text.lower() != "оставить текущее":
            state["data"][field_name] = text
        current_field_index += 1

    if current_field_index < len(state["fields"]):
        next_field = state["fields"][current_field_index]
        await update.message.reply_text(f"Введите значение для поля: {next_field}
(или отправьте 'оставить текущее')")
    else:
        filepath = generate_pdf(state["template"], state["data"])
        with open(filepath, "rb") as f:
            await update.message.reply_document(document=InputFile(f, filename=os.path.basename(filepath)))
        await update.message.reply_text("Готово! Можете начать заново с /start", reply_markup=ReplyKeyboardRemove())
        del user_state[user_id]

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

@fastapi_app.on_event("startup")
async def on_startup():
    await app.bot.set_webhook(WEBHOOK_URL)
    asyncio.create_task(app.initialize())
    asyncio.create_task(app.start())

@fastapi_app.on_event("shutdown")
async def on_shutdown():
    await app.shutdown()
