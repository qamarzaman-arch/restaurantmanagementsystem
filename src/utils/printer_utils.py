from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QTextDocument, QFont
from PyQt6.QtCore import Qt

class PrinterUtils:
    @staticmethod
    def get_available_printers():
        from PyQt6.QtPrintSupport import QPrinterInfo
        return [printer.printerName() for printer in QPrinterInfo.availablePrinters()]

    @staticmethod
    def print_receipt(order_data, settings, printer_name=None):
        """
        Formats and prints a receipt to a thermal printer.
        If printer_name is None, it uses the default printer.
        """
        report_text = PrinterUtils._format_receipt_text(order_data, settings)

        doc = QTextDocument()
        # Set a fixed-width font for receipt alignment
        font = QFont("Courier", 10)
        doc.setDefaultFont(font)
        doc.setPlainText(report_text)

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        if printer_name:
            printer.setPrinterName(printer_name)

        # In a real environment, we might want to set page size to something like 80mm
        # printer.setPageSize(QPageSize(QSizeF(80, 297), QPageSize.Unit.Millimeter))

        doc.print(printer)

    @staticmethod
    def _format_receipt_text(order_data, settings):
        restaurant_name = settings.get('restaurant_name', 'Restaurant POS')
        address = settings.get('address', '')
        phone = settings.get('phone', '')
        tax_rate = float(settings.get('tax_rate', 0))

        width = 32  # Typical for 58mm printer

        lines = []
        lines.append(restaurant_name.center(width))
        if address:
            lines.append(address.center(width))
        if phone:
            lines.append(phone.center(width))
        lines.append("-" * width)

        lines.append(f"Order: {order_data['id']}".ljust(width))
        lines.append(f"Date: {order_data['created_at'][:16]}".ljust(width))
        lines.append(f"Table: {order_data['table_number']}".ljust(width))
        lines.append("-" * width)

        lines.append("Item".ljust(16) + "Qty".rjust(4) + "Total".rjust(12))

        for item in order_data['items']:
            name = item['name'][:15]
            qty = str(item['quantity'])
            total = f"{item['price'] * item['quantity']:.2f}"
            lines.append(name.ljust(16) + qty.rjust(4) + total.rjust(12))

        lines.append("-" * width)
        lines.append(f"Subtotal:".ljust(20) + f"{order_data['subtotal']:.2f}".rjust(12))
        lines.append(f"Tax ({tax_rate}%):".ljust(20) + f"{order_data['tax']:.2f}".rjust(12))
        if order_data['discount'] > 0:
            lines.append(f"Discount:".ljust(20) + f"-{order_data['discount']:.2f}".rjust(12))
        lines.append(f"TOTAL:".ljust(20) + f"{order_data['total']:.2f}".rjust(12))
        lines.append("-" * width)
        lines.append("Thank you for your visit!".center(width))

        return "\n".join(lines)
