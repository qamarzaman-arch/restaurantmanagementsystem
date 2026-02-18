from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QTextDocument, QFont
from PyQt6.QtCore import Qt
import datetime

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
        PrinterUtils._print_text(report_text, printer_name)

    @staticmethod
    def print_kot(order_data, printer_name=None):
        """
        Formats and prints a Kitchen Order Ticket (KOT).
        """
        kot_text = PrinterUtils._format_kot_text(order_data)
        PrinterUtils._print_text(kot_text, printer_name)

    @staticmethod
    def _print_text(text, printer_name=None):
        doc = QTextDocument()
        # Set a fixed-width font for receipt alignment
        font = QFont("Courier", 10)
        doc.setDefaultFont(font)
        doc.setPlainText(text)

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        if printer_name:
            printer.setPrinterName(printer_name)

        doc.print(printer)

    @staticmethod
    def _format_kot_text(order_data):
        width = 32
        lines = []
        lines.append("KITCHEN ORDER TICKET".center(width))
        lines.append("-" * width)
        lines.append(f"Order ID: {order_data['id']}".ljust(width))
        lines.append(f"Table: {order_data.get('table_number', 'N/A')}".ljust(width))
        lines.append(f"Time: {datetime.datetime.now().strftime('%H:%M:%S')}".ljust(width))
        lines.append("-" * width)
        lines.append("Item".ljust(25) + "Qty".rjust(7))
        lines.append("-" * width)

        for item in order_data['items']:
            name = item['name'][:24]
            qty = str(item['quantity'])
            lines.append(name.ljust(25) + qty.rjust(7))

        lines.append("-" * width)
        lines.append("FOR KITCHEN USE ONLY".center(width))
        return "\n".join(lines)

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
        lines.append(f"TOTAL (Rs.):".ljust(20) + f"{order_data['total']:.2f}".rjust(12))
        lines.append("-" * width)
        lines.append("Thank you for your visit!".center(width))

        return "\n".join(lines)
