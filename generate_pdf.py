
from fpdf import FPDF
import os
from datetime import datetime

def generate_pdf(template_name, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", "", 14)

    pdf.cell(0, 10, txt=f"{template_name}", ln=True, align="C")
    pdf.ln(5)
    for key, value in data.items():
        pdf.multi_cell(0, 10, txt=f"{key}: {value}")
        pdf.ln(1)

    pdf.ln(10)
    pdf.multi_cell(0, 10, txt="📞 +37455987715")
    pdf.multi_cell(0, 10, txt="📢 Подписывайтесь на наш Telegram-канал")
    pdf.multi_cell(0, 10, txt="Telegram: @ginekolog_yerevan")

    os.makedirs("tmp", exist_ok=True)
    filename = f"tmp/{data.get('ФИО', 'протокол')}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    pdf.output(filename)
    return filename
