from fpdf import FPDF
import os
from datetime import datetime

def generate_pdf(template, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", "", 14)

    pdf.cell(200, 10, txt=f"🌸 {template}", ln=True, align='C')
    pdf.ln(10)

    for field, value in data.items():
        pdf.multi_cell(0, 10, txt=f"{field}: {value}")

    pdf.ln(10)
    pdf.multi_cell(0, 10, txt="Куриленко Ю.С.")
    pdf.multi_cell(0, 10, txt="📞 +37455987715"
Telegram: "@ginekolog_yerevan")

    filename = f"tmp/{data.get('ФИО', 'протокол').replace(' ', '_')}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    os.makedirs("tmp", exist_ok=True)
    pdf.output(filename)
    return filename
