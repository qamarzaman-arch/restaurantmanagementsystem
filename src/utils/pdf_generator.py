from reportlab.lib.pagesizes import A6
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

class PDFGenerator:
    @staticmethod
    def generate_invoice(order, settings, filename):
        doc = SimpleDocTemplate(filename, pagesize=A6, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
        elements = []
        styles = getSampleStyleSheet()

        # Header
        elements.append(Paragraph(f"<b>{settings.get('restaurant_name', 'Restaurant')}</b>", styles['Title']))
        elements.append(Paragraph(settings.get('address', ''), styles['Normal']))
        elements.append(Spacer(1, 10))

        # Order Info
        elements.append(Paragraph(f"Order ID: {order['id']}", styles['Normal']))
        elements.append(Paragraph(f"Date: {order['created_at']}", styles['Normal']))
        if order.get('table_id'):
            elements.append(Paragraph(f"Table: {order.get('table_id')}", styles['Normal']))
        elements.append(Spacer(1, 10))

        # Items Table
        data = [["Item", "Qty", "Price", "Total"]]
        for item in order['items']:
            data.append([
                item['name'],
                str(item['quantity']),
                f"{item['price']:.2f}",
                f"{(item['price'] * item['quantity']):.2f}"
            ])

        t = Table(data, colWidths=[100, 30, 50, 50])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 10))

        # Totals
        elements.append(Paragraph(f"Subtotal: {order['subtotal']:.2f}", styles['Normal']))
        elements.append(Paragraph(f"Discount: {order['discount']:.2f}", styles['Normal']))
        elements.append(Paragraph(f"Tax: {order['tax']:.2f}", styles['Normal']))
        elements.append(Paragraph(f"<b>Total: {order['total']:.2f}</b>", styles['Normal']))
        elements.append(Spacer(1, 10))

        elements.append(Paragraph("Thank you for visiting!", styles['Italic']))

        doc.build(elements)
        return filename
