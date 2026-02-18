from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt

class CustomerManagementScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)

        # Left side: Form
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        form_layout.addWidget(QLabel("<b>Add/Edit Customer</b>"))

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")
        form_layout.addWidget(QLabel("Name"))
        form_layout.addWidget(self.name_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone Number")
        form_layout.addWidget(QLabel("Phone"))
        form_layout.addWidget(self.phone_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        form_layout.addWidget(QLabel("Email"))
        form_layout.addWidget(self.email_input)

        save_btn = QPushButton("Save Customer")
        save_btn.setObjectName("actionButton")
        save_btn.clicked.connect(self.save_customer)
        form_layout.addWidget(save_btn)

        layout.addLayout(form_layout, 1)

        # Right side: Table
        self.customer_table = QTableWidget()
        self.customer_table.setColumnCount(5)
        self.customer_table.setHorizontalHeaderLabels(["ID", "Name", "Phone", "Email", "Points"])
        self.customer_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.customer_table, 3)

        self.refresh_table()

    def refresh_table(self):
        customers = self.db.get_customers()
        self.customer_table.setRowCount(len(customers))
        for i, cust in enumerate(customers):
            self.customer_table.setItem(i, 0, QTableWidgetItem(str(cust['id'])))
            self.customer_table.setItem(i, 1, QTableWidgetItem(cust['name']))
            self.customer_table.setItem(i, 2, QTableWidgetItem(cust['phone']))
            self.customer_table.setItem(i, 3, QTableWidgetItem(cust['email']))
            self.customer_table.setItem(i, 4, QTableWidgetItem(str(cust['points'])))

    def save_customer(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()

        if not name or not phone:
            QMessageBox.warning(self, "Validation Error", "Name and Phone are required")
            return

        try:
            if self.db.add_customer(name, phone, email):
                self.name_input.clear()
                self.phone_input.clear()
                self.email_input.clear()
                self.refresh_table()
                QMessageBox.information(self, "Success", "Customer saved successfully")
            else:
                QMessageBox.warning(self, "Error", "Customer with this phone already exists")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save customer: {str(e)}")
