import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from generate_pdf import generate_pdf

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = FastAPI()
application = Application.builder().token(BOT_TOKEN).build()

user_state = {}

TEMPLATES = {
    "Консультативное заключение": [
        "ФИО", "Возраст", "Диагноз", "Обследование", "Рекомендации"
    ],
    "УЗИ малого таза": [
        "ФИО", "Дата последней менструации", "Положение матки", "Форма матки",
        "Размеры матки", "Структура миометрия", "М-эхо", "Шейка матки",
        "Яичники", "Дополнительные образования", "Свободная жидкость",
        "Заключение", "Рекомендации"
    ]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[template] for template in TEMPLATES.keys()]
    await update.message.reply_text("Выберите шаблон:", reply_markup={"keyboard": keyboard, "one_time_keyboard": True})
    user_state[update.effective_user.id] = {"stage": "choose"}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_state:
        await update.message.reply_text("Нажмите /start для начала")
        return

    state = user_state[user_id]
    if state["stage"] == "choose":
        if text in TEMPLATES:
            state["template"] = text
            state["fields"] = TEMPLATES[text]
            state["data"] = {}
            state["field_index"] = 0
            state["stage"] = "fill"
            await update.message.reply_text(f"{state['fields'][0]}:")
        else:
            await update.message.reply_text("Пожалуйста, выберите шаблон из списка.")
    elif state["stage"] == "fill":
        field = state["fields"][state["field_index"]]
        state["data"][field] = text
        state["field_index"] += 1
        if state["field_index"] < len(state["fields"]):
            next_field = state["fields"][state["field_index"]]
            await update.message.reply_text(f"{next_field}:")
        else:
            filepath = generate_pdf(state["template"], state["data"])
            await context.bot.send_document(chat_id=update.effective_chat.id, document=open(filepath, "rb"))
            user_state.pop(user_id)

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

@app.on_event("startup")
async def startup():
    await application.initialize()
    await application.start()
    await application.bot.set_webhook(WEBHOOK_URL)

@app.on_event("shutdown")
async def shutdown():
    await application.stop()
    await application.shutdown()
