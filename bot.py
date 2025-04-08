from telegram import Update, InputFile, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from fastapi import FastAPI
import os
from generate_pdf import generate_pdf

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = ApplicationBuilder().token(BOT_TOKEN).build()
fastapi_app = FastAPI()

user_state = {}

templates = {
    "Консультативное заключение": [
        "ФИО", "Возраст", "Диагноз", "Обследование", "Рекомендации"
    ],
    "УЗИ малого таза": [
        "ФИО", "Дата последней менструации", "Положение матки", "Размеры матки",
        "Структура миометрия", "М-эхо", "Состояние шейки", "Размеры яичников",
        "Доп. образования", "Свободная жидкость", "Заключение", "Рекомендации"
    ]
}

@fastapi_app.on_event("startup")
async def startup():
    await app.bot.set_webhook(WEBHOOK_URL)

@fastapi_app.on_event("shutdown")
async def shutdown():
    await app.shutdown()

@app.command_handler("start")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[k] for k in templates] + [["🛑 Стоп"]]
    await update.message.reply_text(
        "Выберите шаблон:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )

@app.message_handler(filters.TEXT)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "🛑 Стоп":
        user_state.pop(user_id, None)
        await update.message.reply_text("⛔️ Ввод прерван.", reply_markup=ReplyKeyboardRemove())
        return

    if user_id not in user_state:
        if text in templates:
            user_state[user_id] = {"template": text, "fields": templates[text], "data": []}
            await update.message.reply_text(f"Введите значение для: {templates[text][0]}")
        else:
            await update.message.reply_text("Пожалуйста, выберите шаблон из списка.")
    else:
        state = user_state[user_id]
        state["data"].append(text)
        if len(state["data"]) < len(state["fields"]):
            next_field = state["fields"][len(state["data"])]
            await update.message.reply_text(f"Введите значение для: {next_field}")
        else:
            filepath = generate_pdf(state["template"], dict(zip(state["fields"], state["data"])))
            await update.message.reply_document(document=InputFile(filepath))
            user_state.pop(user_id)

def main():
    import uvicorn
    uvicorn.run(fastapi_app, host="0.0.0.0", port=10000)

if __name__ == "__main__":
    main()