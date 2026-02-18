from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QDateEdit, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, QDate
import csv
import os

class ReportsScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Filters
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("From:"))
        self.date_from = QDateEdit(QDate.currentDate().addDays(-7))
        self.date_from.setCalendarPopup(True)
        filter_layout.addWidget(self.date_from)

        filter_layout.addWidget(QLabel("To:"))
        self.date_to = QDateEdit(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        filter_layout.addWidget(self.date_to)

        refresh_btn = QPushButton("Filter")
        refresh_btn.clicked.connect(self.refresh_report)
        filter_layout.addWidget(refresh_btn)

        export_btn = QPushButton("Export to CSV")
        export_btn.clicked.connect(self.export_csv)
        filter_layout.addWidget(export_btn)

        layout.addLayout(filter_layout)

        # Report Table
        self.report_table = QTableWidget()
        self.report_table.setColumnCount(5)
        self.report_table.setHorizontalHeaderLabels(["Date", "Order ID", "Type", "Payment", "Total"])
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.report_table)

        self.summary_label = QLabel("<b>Total Sales: Rs. 0.00</b>")
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.summary_label)

        # Advanced Insights
        insights_frame = QFrame()
        insights_frame.setStyleSheet("background-color: #ecf0f1; border-radius: 5px; padding: 10px;")
        self.insights_layout = QHBoxLayout(insights_frame)
        self.avg_order_label = QLabel("Avg Order: Rs. 0.00")
        self.most_popular_label = QLabel("Popular: N/A")
        self.insights_layout.addWidget(self.avg_order_label)
        self.insights_layout.addWidget(self.most_popular_label)
        layout.addWidget(insights_frame)

        self.refresh_report()

    def refresh_report(self):
        d_from = self.date_from.date().toString("yyyy-MM-dd")
        d_to = self.date_to.date().toString("yyyy-MM-dd")

        orders = self.db.get_all_orders(status='Completed', date_from=d_from, date_to=d_to)
        self.report_table.setRowCount(len(orders))
        total = 0
        for i, order in enumerate(orders):
            self.report_table.setItem(i, 0, QTableWidgetItem(order['created_at']))
            self.report_table.setItem(i, 1, QTableWidgetItem(str(order['id'])))
            self.report_table.setItem(i, 2, QTableWidgetItem(order['order_type']))
            self.report_table.setItem(i, 3, QTableWidgetItem(order['payment_method']))
            self.report_table.setItem(i, 4, QTableWidgetItem(f"{order['total']:.2f}"))
            total += order['total']

        self.summary_label.setText(f"<b>Total Sales: Rs. {total:.2f}</b>")
        self.current_orders = orders

        # Update Insights
        if orders:
            avg = total / len(orders)
            self.avg_order_label.setText(f"Avg Order: Rs. {avg:.2f}")

            top_items = self.db.get_top_selling_items(1)
            if top_items:
                self.most_popular_label.setText(f"Most Popular: {top_items[0]['name']}")
        else:
            self.avg_order_label.setText("Avg Order: Rs. 0.00")
            self.most_popular_label.setText("Most Popular: N/A")

    def export_csv(self):
        if not hasattr(self, 'current_orders') or not self.current_orders:
            QMessageBox.warning(self, "No Data", "No data to export")
            return

        os.makedirs("reports", exist_ok=True)
        filename = "reports/sales_report.csv"
        try:
            with open(filename, 'w', newline='') as f:
                if not self.current_orders: return
                writer = csv.DictWriter(f, fieldnames=self.current_orders[0].keys())
                writer.writeheader()
                writer.writerows(self.current_orders)
            QMessageBox.information(self, "Export Successful", f"Report saved to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export CSV: {str(e)}")
