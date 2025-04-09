
from fastapi import FastAPI, Request
import os
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from fpdf import FPDF

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telegram.Bot(token=TOKEN)
app = FastAPI()
dispatcher = Dispatcher(bot, None, workers=0)

user_data = {}

def start(update, context):
    keyboard = [
        [InlineKeyboardButton("🧾 Консультативное заключение", callback_data='consult')],
        [InlineKeyboardButton("📷 УЗИ для беременных", callback_data='us_pregnancy')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите шаблон:", reply_markup=reply_markup)

def stop(update, context):
    user_data.pop(update.effective_chat.id, None)
    update.message.reply_text("Ввод остановлен.")

def button(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id
    user_data[chat_id] = {}

    if query.data == "consult":
        user_data[chat_id]["template"] = "consult"
        user_data[chat_id]["fields"] = [
            "Дата", "ФИО", "Возраст", "Диагноз", "Обследование", "Рекомендации"
        ]
    elif query.data == "us_pregnancy":
        user_data[chat_id]["template"] = "us_pregnancy"
        user_data[chat_id]["fields"] = [
            "ФИО", "Последняя менструация", "Положение матки", "Размер плодного яйца",
            "Размер эмбриона", "Желточный мешок", "Сердцебиение и ЧСС", "Расположение хориона",
            "Желтое тело", "Дополнительные данные", "Заключение", "Рекомендации"
        ]

    user_data[chat_id]["answers"] = []
    bot.send_message(chat_id=chat_id, text=f"Введите: {user_data[chat_id]['fields'][0]}")

def handle_message(update, context):
    chat_id = update.message.chat_id
    if chat_id not in user_data:
        update.message.reply_text("Напишите /start, чтобы начать.")
        return

    data = user_data[chat_id]
    data["answers"].append(update.message.text)

    if len(data["answers"]) < len(data["fields"]):
        next_field = data["fields"][len(data["answers"])]
        bot.send_message(chat_id=chat_id, text=f"Введите: {next_field}")
    else:
        filename = f"/mnt/data/consultation_{chat_id}.pdf"
        generate_pdf(data["template"], data["fields"], data["answers"], filename)
        with open(filename, "rb") as f:
            bot.send_document(chat_id=chat_id, document=f)
        bot.send_message(chat_id=chat_id, text="Готово ✅")
        user_data.pop(chat_id)

def generate_pdf(template, fields, answers, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf.cell(200, 10, txt="🌸 Док Куриленко", ln=True, align="C")
    pdf.set_font("DejaVu", style='U', size=12)
    pdf.cell(200, 10, txt="Консультативное заключение" if template == "consult" else "УЗИ для беременных", ln=True, align="C")
    pdf.set_font("DejaVu", size=12)
    pdf.ln(10)

    for field, answer in zip(fields, answers):
        pdf.multi_cell(0, 10, f"{field}: {answer}", align="L")

    pdf.ln(5)
    pdf.cell(0, 10, txt="Телефон: +37455987715", ln=True)
    pdf.cell(0, 10, txt="Telegram: t.me/dok_kurilenko", ln=True)
    pdf.ln(10)
    pdf.cell(0, 10, txt="Куриленко Ю.С.", ln=True, align="R")

    pdf.output(filename)

@app.post("/webhook")
async def process_webhook(request: Request):
    update = telegram.Update.de_json(await request.json(), bot)
    dispatcher.process_update(update)
    return "ok"

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("stop", stop))
dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
