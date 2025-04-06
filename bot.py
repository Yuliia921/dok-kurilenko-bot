import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Док Куриленко здесь 🌸")

# Запуск бота
def main():
    app = ApplicationBuilder().token("7495233579:AAGKqPpZY0vd3ZK9a1ljAbZjEehCCMhFIdU").build()
    app.add_handler(CommandHandler("start", start))
    logger.info("✅ Бот запущен (без Flask)")
    app.run_polling()

if __name__ == "__main__":
    main()
