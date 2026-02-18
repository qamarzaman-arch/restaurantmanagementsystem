from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QSpinBox, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt

class TableManagementScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)

        # Left side: Form
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        form_layout.addWidget(QLabel("<b>Add Table</b>"))

        self.table_num = QLineEdit()
        self.table_num.setPlaceholderText("Table Number (e.g. T1)")
        form_layout.addWidget(QLabel("Table Number"))
        form_layout.addWidget(self.table_num)

        self.capacity = QSpinBox()
        self.capacity.setMinimum(1)
        self.capacity.setValue(4)
        form_layout.addWidget(QLabel("Capacity"))
        form_layout.addWidget(self.capacity)

        add_btn = QPushButton("Add Table")
        add_btn.setObjectName("actionButton")
        add_btn.clicked.connect(self.add_table)
        form_layout.addWidget(add_btn)

        layout.addLayout(form_layout, 1)

        # Right side: Table List
        self.tables_list = QTableWidget()
        self.tables_list.setColumnCount(3)
        self.tables_list.setHorizontalHeaderLabels(["ID", "Number", "Capacity"])
        self.tables_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tables_list, 2)

        self.refresh_table()

    def refresh_table(self):
        tables = self.db.get_tables()
        self.tables_list.setRowCount(len(tables))
        for i, table in enumerate(tables):
            self.tables_list.setItem(i, 0, QTableWidgetItem(str(table['id'])))
            self.tables_list.setItem(i, 1, QTableWidgetItem(table['table_number']))
            self.tables_list.setItem(i, 2, QTableWidgetItem(str(table['capacity'])))

    def add_table(self):
        num = self.table_num.text().strip()
        cap = self.capacity.value()
        if not num:
            QMessageBox.warning(self, "Validation Error", "Table number cannot be empty")
            return

        try:
            if self.db.add_table(num, cap):
                self.table_num.clear()
                self.refresh_table()
            else:
                QMessageBox.warning(self, "Error", f"Table '{num}' already exists")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to add table: {str(e)}")
