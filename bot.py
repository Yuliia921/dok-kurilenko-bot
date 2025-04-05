
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🧼 Минимальный бот запускается...")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ /start получен")
    await update.message.reply_text("Бот работает! 🌸")

async def main():
    app = ApplicationBuilder().token("7591394007:AAHBZWhMJgpmnKY85suJaJ5AW_RpwPTZ9VI").build()
    app.add_handler(CommandHandler("start", start))

    await app.bot.delete_webhook(drop_pending_updates=True)
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
