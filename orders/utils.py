from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_invoice(order):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 50, "MyVastra - Invoice")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 100, f"Order ID: {order.id}")
    p.drawString(50, height - 120, f"Customer: {order.name}")
    p.drawString(50, height - 140, f"Phone: {order.phone}")
    p.drawString(50, height - 160, f"Address: {order.address}")
    p.drawString(50, height - 180, f"Date: {order.ordered_at.strftime('%d %b %Y %H:%M')}")

    y = height - 220
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Item")
    p.drawString(300, y, "Qty")
    p.drawString(350, y, "Price")
    p.drawString(420, y, "Total")
    y -= 20

    p.setFont("Helvetica", 11)
    for item in order.items.all():
        p.drawString(50, y, item.product.name)
        p.drawString(300, y, str(item.quantity))
        p.drawString(350, y, f"₹{item.price}")
        p.drawString(420, y, f"₹{item.quantity * item.price}")
        y -= 20

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y - 10, f"Total: ₹{order.total_price}")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
