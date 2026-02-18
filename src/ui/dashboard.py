from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QGridLayout)
from PyQt6.QtCore import Qt

class DashboardScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h1 style='color: #2c3e50;'>Dashboard</h1>"))

        stats_layout = QGridLayout()

        self.total_sales = self.create_stat_card("Total Sales Today", "0.00")
        self.total_orders = self.create_stat_card("Orders Today", "0")
        self.active_tables = self.create_stat_card("Active Tables", "0")

        stats_layout.addWidget(self.total_sales, 0, 0)
        stats_layout.addWidget(self.total_orders, 0, 1)
        stats_layout.addWidget(self.active_tables, 0, 2)

        layout.addLayout(stats_layout)
        layout.addStretch()

        self.refresh_stats()

    def create_stat_card(self, title, value):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #dcdde1;
                padding: 20px;
            }
        """)
        layout = QVBoxLayout(frame)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        layout.addWidget(title_label)

        value_label = QLabel(value)
        value_label.setStyleSheet("color: #2c3e50; font-size: 24px; font-weight: bold;")
        layout.addWidget(value_label)

        frame.value_label = value_label
        return frame

    def refresh_stats(self):
        orders = self.db.get_all_orders(status='Completed')
        # Simple today filter (ignoring actual date for demo, but in real app would filter by current date)
        total_revenue = sum(o['total'] for o in orders)
        count = len(orders)

        tables = self.db.get_tables()
        active = len([t for t in tables if t['status'] == 'Occupied'])

        self.total_sales.value_label.setText(f"${total_revenue:.2f}")
        self.total_orders.value_label.setText(str(count))
        self.active_tables.value_label.setText(str(active))
