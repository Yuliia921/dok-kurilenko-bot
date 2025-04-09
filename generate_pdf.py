from fpdf import FPDF
import os
from datetime import datetime

def generate_pdf(fields: dict, template_name: str) -> str:
    pdf = FPDF()
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVuB", "", "DejaVuSans-Bold.ttf", uni=True)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("DejaVuB", "", 14)
    pdf.cell(0, 10, "🌸 Док Куриленко", ln=True, align="C")
    pdf.set_font("DejaVu", "", 12)
    pdf.multi_cell(0, 10, template_name, align="C")
    pdf.ln(5)

    for key, value in fields.items():
        text = f"{key}: {value}"
        try:
            pdf.multi_cell(0, 10, text, align="L", max_line_height=pdf.font_size)
        except:
            # fallback: вручную разбиваем слишком длинные строки
            wrapped = text[:90] + "..." if len(text) > 90 else text
            pdf.multi_cell(0, 10, wrapped, align="L")

    pdf.ln(5)
    pdf.cell(0, 10, "Врач акушер-гинеколог Куриленко Юлия Сергеевна", ln=True)
    pdf.cell(0, 10, "+37455987715", ln=True)
    pdf.cell(0, 10, "Telegram: https://t.me/doc_Kurilenko", ln=True)

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Куриленко_Юлия_{now}.pdf"
    filepath = os.path.join("tmp", filename)
    os.makedirs("tmp", exist_ok=True)
    pdf.output(filepath)

    return filepath