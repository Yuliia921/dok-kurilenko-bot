import os
import logging
import telegram
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from generate_pdf import generate_pdf
from io import BytesIO
import fpdf
print(">>> fpdf version:", fpdf.__version__)

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ Переменная окружения BOT_TOKEN не задана! Укажите её в настройках Render.")

app = Application.builder().token(BOT_TOKEN).build()

templates = {
    "Консультативное заключение": [
        "ФИО", "Возраст", "Диагноз", "Обследование", "Рекомендации"
    ],
    "УЗИ малого таза": [
        "ФИО", "Дата последней менструации", "Матка (положение, форма, размеры, структура)",
        "М-эхо", "Шейка матки", "Правый яичник", "Левый яичник",
        "Дополнительные образования", "Свободная жидкость", "Заключение", "Рекомендации"
    ]
}

user_state = {}

@app.post_init
async def startup(app): print("✅ Бот запущен и готов к работе")

@app.on_message(filters.COMMAND)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[k] for k in templates]
    await update.message.reply_text(
        "Выберите шаблон:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )

@app.on_message(filters.TEXT & ~filters.COMMAND)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_state:
        if text in templates:
            user_state[user_id] = {"template": text, "data": {}}
            field = templates[text][0]
            await update.message.reply_text(f"Введите значение поля: {field}")
        else:
            await update.message.reply_text("Пожалуйста, выберите шаблон из меню.")
    else:
        state = user_state[user_id]
        template = state["template"]
        fields = templates[template]
        data = state["data"]
        current_index = len(data)
        data[fields[current_index]] = text

        if current_index + 1 < len(fields):
            next_field = fields[current_index + 1]
            await update.message.reply_text(f"Введите значение поля: {next_field}")
        else:
            filepath = generate_pdf(data)
            with open(filepath, "rb") as f:
                pdf_bytes = BytesIO(f.read())
                pdf_bytes.name = os.path.basename(filepath)
                await context.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=pdf_bytes
                )
            del user_state[user_id]

app.run_polling()