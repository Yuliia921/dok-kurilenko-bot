from fpdf import FPDF
import os
from datetime import datetime

def generate_pdf(template_name, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf.set_font("DejaVu", style="B", size=14)
    pdf.cell(0, 10, template_name + " 🌸", ln=True, align="C")
    pdf.set_font("DejaVu", size=12)
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    for key, value in data.items():
        pdf.set_font("DejaVu", style="B", size=12)
        pdf.cell(60, 10, f"{key}:", ln=0)
        pdf.set_font("DejaVu", style="", size=12)
        pdf.multi_cell(0, 10, value)

    pdf.ln(10)
    pdf.set_font("DejaVu", style="", size=11)
    pdf.cell(0, 10, "Врач акушер-гинеколог Куриленко Юлия Сергеевна", ln=True)
    pdf.cell(0, 10, "+37455987715", ln=True)
    pdf.cell(0, 10, "Telegram: https://t.me/doc_Kurilenko", ln=True)

    filename = f"{data.get('ФИО', 'протокол')}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    path = os.path.join("tmp", filename)
    os.makedirs("tmp", exist_ok=True)
    pdf.output(path)
    return path
