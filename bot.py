import os
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from generate_pdf import generate_pdf

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

templates = {
    "Консультативное заключение": ["Дата", "ФИО", "Возраст", "Диагноз", "Обследование", "Рекомендации"],
    "УЗИ органов малого таза": ["ФИО", "Дата последней менструации", "Положение матки", "Размеры матки", "Структура миометрия", "M-echo", "Состояние шейки матки", "Размеры яичников", "Фолликулы", "Дополнительно", "Свободная жидкость", "Заключение", "Рекомендации"]
}

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[k] for k in templates.keys()] + [["🛑 Стоп"]]
    await update.message.reply_text("Выберите шаблон:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_state:
        del user_state[user_id]
    await update.message.reply_text("⛔️ Ввод остановлен. Используйте /start для начала заново.", reply_markup=ReplyKeyboardRemove())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if text == "🛑 Стоп":
        await stop(update, context)
        return

    if user_id not in user_state:
        if text in templates:
            user_state[user_id] = {"template": text, "data": {}, "step": 0}
            await update.message.reply_text(f"Введите: {templates[text][0]}", reply_markup=ReplyKeyboardRemove())
        else:
            await update.message.reply_text("Пожалуйста, выберите шаблон с помощью /start")
        return

    state = user_state[user_id]
    template = state["template"]
    field_name = templates[template][state["step"]]
    state["data"][field_name] = text
    state["step"] += 1

    if state["step"] < len(templates[template]):
        next_field = templates[template][state["step"]]
        await update.message.reply_text(f"Введите: {next_field}")
    else:
        filepath = generate_pdf(template, state["data"])
        with open(filepath, "rb") as f:
            await update.message.reply_document(document=InputFile(f), filename=os.path.basename(filepath))
        del user_state[user_id]

def main():
    if not TOKEN or not WEBHOOK_URL:
        raise ValueError("❌ Установите переменные окружения BOT_TOKEN и WEBHOOK_URL!")

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    from fastapi import FastAPI
    fastapi_app = FastAPI()

    @fastapi_app.get("/")
    async def root():
        return {"status": "OK"}

    @fastapi_app.on_event("startup")
    async def on_startup():
        await application.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
        await application.initialize()
        await application.start()
        await application.updater.start_polling()

    @fastapi_app.on_event("shutdown")
    async def on_shutdown():
        await application.updater.stop()
        await application.stop()
        await application.shutdown()

    from telegram.ext import webhook
    fastapi_app.add_route("/webhook", webhook.WebhookHandler(application))

    import uvicorn
    uvicorn.run(fastapi_app, host="0.0.0.0", port=10000)

if __name__ == "__main__":
    main()