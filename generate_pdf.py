from fpdf import FPDF
import os
from datetime import datetime

def generate_pdf(fields: dict) -> str:
    fio = fields.get("ФИО", "consultation").replace(" ", "_")
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{fio}_{date}.pdf"

    os.makedirs("tmp", exist_ok=True)
    path = os.path.join("tmp", filename)

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVu", "B", "DejaVuSans-Bold.ttf", uni=True)
    pdf.set_font("DejaVu", size=16)
    pdf.cell(0, 10, txt="🌸 Медицинский протокол", ln=True, align="C")
    pdf.line(10, 20, 200, 20)
    pdf.ln(10)

    for k, v in fields.items():
        pdf.set_font("DejaVu", style="B", size=12)
        pdf.cell(60, 10, txt=f"{k}:", ln=0)
        pdf.set_font("DejaVu", size=12)
        pdf.multi_cell(0, 10, txt=v)
        pdf.ln(2)

    pdf.ln(8)
    pdf.set_font("DejaVu", size=12)
    pdf.cell(0, 10, txt="Врач акушер-гинеколог Куриленко Юлия Сергеевна", ln=True)
    pdf.set_font("DejaVu", size=10)
    pdf.cell(0, 8, txt="📞 +37455987715", ln=True)
    pdf.cell(0, 8, txt="Telegram: https://t.me/doc_Kurilenko", ln=True)

    pdf.output(path)
    return path