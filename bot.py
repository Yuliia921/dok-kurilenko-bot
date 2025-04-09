import os
import logging
from io import BytesIO
import telegram
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.error import Conflict
from generate_pdf import generate_pdf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
user_data = {}

TEMPLATES = {
    "Консультативное заключение": ["ФИО", "Возраст", "Диагноз", "Обследование", "Рекомендации"],
    "УЗИ для беременных": [
        "ФИО", "Последняя менструация", "Положение матки", "Размер плодного яйца",
        "Размер эмбриона", "Желточный мешок", "Сердцебиение и ЧСС", "Расположение хориона",
        "Желтое тело", "Дополнительные данные", "Заключение", "Рекомендации"
    ]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[key] for key in TEMPLATES]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Добро пожаловать в Док Куриленко 🌸\nВыберите шаблон:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.effective_chat.id

    if text in TEMPLATES:
        user_data[chat_id] = {
            "шаблон": text,
            "поля": {},
            "шаг": 0,
            "список_полей": TEMPLATES[text]
        }
        await update.message.reply_text(f"Введите {TEMPLATES[text][0]}:")
    elif chat_id in user_data:
        data = user_data[chat_id]
        шаг = data["шаг"]
        поля = data["список_полей"]

        if шаг < len(поля):
            data["поля"][поля[шаг]] = text
            data["шаг"] += 1
            if data["шаг"] < len(поля):
                await update.message.reply_text(f"Введите {поля[data['шаг']]}:")
            else:
                filepath = generate_pdf(data["поля"])
                file_size = os.path.getsize(filepath)
                logger.info(f"📄 PDF создан: {filepath}, размер: {file_size} байт")
                await update.message.reply_document(
                    document=BytesIO(open(filepath, 'rb').read()), filename=os.path.basename(filepath),
                    caption=f"{data['шаблон']} 🌸"
                )
                del user_data[chat_id]
        else:
            await update.message.reply_text("Шаблон завершён.")
    else:
        await update.message.reply_text("Пожалуйста, начните с команды /start")

if __name__ == "__main__":
    try:
        telegram.Bot(token=BOT_TOKEN).delete_webhook(drop_pending_updates=True)
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app.run_polling()
    except Conflict as e:
        logger.error("❌ Конфликт: бот уже работает где-то ещё. Завершение.")
    except Exception as e:
        logger.exception(f"❌ Ошибка при запуске: {e}")