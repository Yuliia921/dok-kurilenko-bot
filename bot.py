
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🚀 Старт чистого бота в главном потоке...")

# Хэндлеры
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("✅ Получена команда /start")
    await update.message.reply_text("Привет от Док Куриленко 🌸 Бот теперь точно живой!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"📩 Сообщение от пользователя: {update.message.text}")
    await update.message.reply_text("Я вас услышал 🌸")

def main():
    app = ApplicationBuilder().token("7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()

if __name__ == "__main__":
    main()
