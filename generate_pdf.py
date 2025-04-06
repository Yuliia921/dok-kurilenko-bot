from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf(fields: dict) -> str:
    path = "/mnt/data/consultation.pdf"
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 80, "Консультативное заключение")
    c.line(70, height - 85, width - 70, height - 85)

    c.setFont("Helvetica", 12)
    y = height - 120
    for k, v in fields.items():
        c.drawString(70, y, f"{k}: {v}")
        y -= 25

    c.setFont("Helvetica", 10)
    c.drawString(70, y - 10, "📞 +37455987715")
    c.drawString(70, y - 30, "🔗 https://t.me/doc_Kurilenko")

    c.setFont("Helvetica-Oblique", 11)
    c.drawString(70, y - 60, "Врач акушер-гинеколог Куриленко Юлия Сергеевна")

    c.save()
    return path
