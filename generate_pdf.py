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
    pdf.cell(0, 10, template_name, ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("DejaVuB", "", 12)
    pdf.cell(0, 10, "🧠 Матка и структуры", ln=True)
    pdf.set_font("DejaVu", "", 12)
    pdf.multi_cell(180, 10, f"Положение матки: {fields.get('Положение матки', '')}", align="L")
    pdf.multi_cell(180, 10, f"Размер плодного яйца: {fields.get('Размер плодного яйца', '')}", align="L")
    pdf.multi_cell(180, 10, f"Размер эмбриона: {fields.get('Размер эмбриона', '')}", align="L")
    pdf.multi_cell(180, 10, f"Желточный мешок: {fields.get('Желточный мешок', '')}", align="L")
    pdf.multi_cell(180, 10, f"Расположение хориона: {fields.get('Расположение хориона', '')}", align="L")
    pdf.multi_cell(180, 10, f"Желтое тело: {fields.get('Желтое тело', '')}", align="L")

    pdf.ln(3)
    pdf.set_font("DejaVuB", "", 12)
    pdf.cell(0, 10, "👶 Плод", ln=True)
    pdf.set_font("DejaVu", "", 12)
    pdf.multi_cell(180, 10, f"Сердцебиение и ЧСС: {fields.get('Сердцебиение и ЧСС', '')}", align="L")

    pdf.ln(3)
    pdf.set_font("DejaVuB", "", 12)
    pdf.cell(0, 10, "📎 Дополнительные данные", ln=True)
    pdf.set_font("DejaVu", "", 12)
    pdf.multi_cell(180, 10, f"{fields.get('Дополнительные данные', '')}", align="L")

    pdf.ln(3)
    pdf.set_font("DejaVuB", "", 12)
    pdf.cell(0, 10, "📌 Заключение", ln=True)
    pdf.set_font("DejaVu", "", 12)
    pdf.multi_cell(180, 10, f"{fields.get('Заключение', '')}", align="L")

    pdf.ln(3)
    pdf.set_font("DejaVuB", "", 12)
    pdf.cell(0, 10, "📋 Рекомендации", ln=True)
    pdf.set_font("DejaVu", "", 12)
    pdf.multi_cell(180, 10, f"{fields.get('Рекомендации', '')}", align="L")

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