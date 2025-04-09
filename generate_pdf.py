from fpdf import FPDF
import os
from datetime import datetime

def generate_pdf(fields: dict, template_name: str) -> str:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVuB", "", "DejaVuSans-Bold.ttf", uni=True)
    pdf.add_page()

    page_width = pdf.w - 2 * pdf.l_margin

    pdf.set_font("DejaVuB", "", 14)
    pdf.multi_cell(page_width, 10, template_name, align="C")
    pdf.ln(5)

    def write_section(title, content_dict, keys):
        pdf.set_font("DejaVuB", "", 12)
        pdf.multi_cell(page_width, 10, title, align="L")
        pdf.set_font("DejaVu", "", 12)
        for key in keys:
            value = content_dict.get(key, "")
            pdf.multi_cell(page_width, 10, f"{key}: {value}", align="L")
        pdf.ln(3)

    # Секции
    write_section("👩 Пациент", fields, ["ФИО", "Последняя менструация"])
    write_section("🧠 Матка и структуры", fields, [
        "Положение матки", "Размер плодного яйца", "Размер эмбриона",
        "Желточный мешок", "Расположение хориона", "Желтое тело"
    ])
    write_section("👶 Плод", fields, ["Сердцебиение и ЧСС"])
    write_section("📎 Дополнительные данные", fields, ["Дополнительные данные"])
    write_section("📌 Заключение", fields, ["Заключение"])
    write_section("📋 Рекомендации", fields, ["Рекомендации"])

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