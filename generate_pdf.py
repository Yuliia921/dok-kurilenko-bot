from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime

def generate_pdf(fields: dict) -> str:
    pdfmetrics.registerFont(TTFont("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
    
    fio = fields.get("ФИО", "consultation").replace(" ", "_")
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{fio}_{date}.pdf"
    path = os.path.join("/mnt/data", filename)

    c = canvas.Canvas(path, pagesize=A4)
    c.setFont("DejaVuSans", 14)
    width, height = A4

    c.drawCentredString(width / 2, height - 50, "Консультативное заключение")
    c.line(50, height - 55, width - 50, height - 55)

    y = height - 90
    c.setFont("DejaVuSans", 12)
    for k, v in fields.items():
        c.drawString(70, y, f"{k}: {v}")
        y -= 25

    y -= 10
    c.drawString(70, y, "Врач акушер-гинеколог Куриленко Юлия Сергеевна")
    y -= 20
    c.setFont("DejaVuSans", 10)
    c.drawString(70, y, "📞 +37455987715")
    y -= 15
    c.drawString(70, y, "Telegram: https://t.me/doc_Kurilenko")

    c.save()
    return path