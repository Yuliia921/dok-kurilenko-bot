import os
import logging
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
user_memory = {}

print("✅ Бот запущен и готов к работе")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[k] for k in templates]
    await update.message.reply_text(
        "Выберите шаблон:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_state:
        if text in templates:
            user_state[user_id] = {"template": text, "data": {}, "step": 0}
            first_field = templates[text][0]
            saved = user_memory.get(user_id, {}).get(first_field)
            if saved:
                await update.message.reply_text(f"{first_field} (текущее: {saved}):")
            else:
                await update.message.reply_text(f"Введите значение поля: {first_field}")
        else:
            await update.message.reply_text("Пожалуйста, выберите шаблон из меню.")
    else:
        state = user_state[user_id]
        template = state["template"]
        fields = templates[template]
        step = state["step"]
        data = state["data"]

        field_name = fields[step]
        if text.strip() == "" and user_memory.get(user_id, {}).get(field_name):
            data[field_name] = user_memory[user_id][field_name]
        else:
            data[field_name] = text.strip()

        step += 1
        state["step"] = step

        if step < len(fields):
            next_field = fields[step]
            saved = user_memory.get(user_id, {}).get(next_field)
            if saved:
                await update.message.reply_text(f"{next_field} (текущее: {saved}):")
            else:
                await update.message.reply_text(f"Введите значение поля: {next_field}")
        else:
            user_memory[user_id] = {
                key: data[key] for key in ["ФИО", "Возраст", "Диагноз"] if key in data
            }
            filepath = generate_pdf(data)
            with open(filepath, "rb") as f:
                pdf_bytes = BytesIO(f.read())
                pdf_bytes.name = os.path.basename(filepath)
                await context.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=pdf_bytes
                )
            del user_state[user_id]

# Регистрируем хендлеры
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()