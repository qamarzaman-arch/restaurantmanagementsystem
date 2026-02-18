from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QFrame)
from PyQt6.QtCore import Qt
from src.utils.pdf_generator import PDFGenerator
from src.utils.printer_utils import PrinterUtils
import os

class OrderHistoryScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h1 style='color: #2c3e50;'>Order History</h1>"))

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(6)
        self.orders_table.setHorizontalHeaderLabels(["ID", "Date", "Type", "Total", "Payment", "Action"])
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.orders_table)

        self.refresh_table()

    def refresh_table(self):
        orders = self.db.get_all_orders()
        self.orders_table.setRowCount(len(orders))
        for i, order in enumerate(orders):
            self.orders_table.setItem(i, 0, QTableWidgetItem(str(order['id'])))
            self.orders_table.setItem(i, 1, QTableWidgetItem(order['created_at']))
            self.orders_table.setItem(i, 2, QTableWidgetItem(order['order_type']))
            self.orders_table.setItem(i, 3, QTableWidgetItem(f"{order['total']:.2f}"))
            self.orders_table.setItem(i, 4, QTableWidgetItem(order['payment_method']))

            reprint_btn = QPushButton("Reprint")
            reprint_btn.clicked.connect(lambda checked, o=order: self.reprint_invoice(o))
            self.orders_table.setCellWidget(i, 5, reprint_btn)

    def reprint_invoice(self, order_summary):
        try:
            order_data = self.db.get_order(order_summary['id'])
            settings = self.db.get_all_settings()

            # Generate PDF
            os.makedirs("invoices", exist_ok=True)
            filename = f"invoices/reprint_{order_data['id']}.pdf"
            PDFGenerator.generate_invoice(order_data, settings, filename)

            # Thermal Print
            printer_name = settings.get('printer_name', 'Default')
            if printer_name == 'Default': printer_name = None
            try:
                PrinterUtils.print_receipt(order_data, settings, printer_name)
                print_msg = "\nReceipt sent to printer."
            except:
                print_msg = "\nThermal printing failed (Check printer)."

            QMessageBox.information(self, "Success", f"Invoice generated: {filename}{print_msg}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to reprint: {str(e)}")
