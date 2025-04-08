
from fpdf import FPDF
from datetime import datetime
import os

def generate_pdf(template_name, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf.set_text_color(0, 0, 0)
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.cell(200, 10, txt=f"🌸 Док Куриленко — {template_name}", ln=True, align="C")
    pdf.ln(10)

    for key, value in data.items():
        pdf.multi_cell(0, 10, txt=f"{key}: {value}")

    pdf.ln(10)
    pdf.multi_cell(0, 10, txt="📞 +37455987715 | Telegram: t.me/doc_kurilenko")

    filename = f"tmp/{data.get('ФИО', 'Протокол')}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    os.makedirs("tmp", exist_ok=True)
    pdf.output(filename)
    return filename
