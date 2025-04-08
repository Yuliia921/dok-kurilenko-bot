from fpdf import FPDF
import os
from datetime import datetime

def generate_pdf(template_name, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)
    
    pdf.multi_cell(0, 10, txt=f"🌸 {template_name}", align="C")
    pdf.ln(10)
    
    for key, value in data.items():
        pdf.multi_cell(0, 10, txt=f"{key}: {value}")
    
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt="📞 +37455987715")
    pdf.multi_cell(0, 10, txt="📢 Подписывайтесь на наш Telegram-канал: @ginekolog_yerevan")
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"tmp/{data.get('ФИО', 'документ')}_{timestamp}.pdf"
    os.makedirs("tmp", exist_ok=True)
    pdf.output(filename)
    return filename