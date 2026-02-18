from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QDoubleSpinBox, QDateEdit, QComboBox)
from PyQt6.QtCore import Qt, QDate

class ExpenseManagementScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)

        # Left side: Form
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        form_layout.addWidget(QLabel("<b>Add New Expense</b>"))

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Expense Title (e.g. Electricity Bill)")
        form_layout.addWidget(QLabel("Title"))
        form_layout.addWidget(self.title_input)

        self.category_combo = QComboBox()
        self.category_combo.addItems(["Utilities", "Rent", "Groceries", "Salaries", "Maintenance", "Others"])
        form_layout.addWidget(QLabel("Category"))
        form_layout.addWidget(self.category_combo)

        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0, 10000000)
        self.amount_input.setPrefix("Rs. ")
        form_layout.addWidget(QLabel("Amount"))
        form_layout.addWidget(self.amount_input)

        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        form_layout.addWidget(QLabel("Date"))
        form_layout.addWidget(self.date_input)

        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Description (Optional)")
        form_layout.addWidget(QLabel("Description"))
        form_layout.addWidget(self.desc_input)

        save_btn = QPushButton("Save Expense")
        save_btn.setObjectName("actionButton")
        save_btn.setMinimumHeight(40)
        save_btn.clicked.connect(self.save_expense)
        form_layout.addWidget(save_btn)

        layout.addLayout(form_layout, 1)

        # Right side: Table
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("<b>Expense List</b>"))

        self.expense_table = QTableWidget()
        self.expense_table.setColumnCount(6)
        self.expense_table.setHorizontalHeaderLabels(["ID", "Date", "Title", "Category", "Amount (Rs.)", "Action"])
        self.expense_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.expense_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) # Title stretches
        right_layout.addWidget(self.expense_table)

        layout.addLayout(right_layout, 2)

        self.refresh_table()

    def refresh_table(self):
        expenses = self.db.get_expenses()
        self.expense_table.setRowCount(len(expenses))
        for i, exp in enumerate(expenses):
            self.expense_table.setItem(i, 0, QTableWidgetItem(str(exp['id'])))
            self.expense_table.setItem(i, 1, QTableWidgetItem(exp['expense_date']))
            self.expense_table.setItem(i, 2, QTableWidgetItem(exp['title']))
            self.expense_table.setItem(i, 3, QTableWidgetItem(exp['category']))
            self.expense_table.setItem(i, 4, QTableWidgetItem(f"{exp['amount']:.2f}"))

            del_btn = QPushButton("Delete")
            del_btn.setObjectName("dangerButton")
            del_btn.clicked.connect(lambda checked, eid=exp['id']: self.delete_expense(eid))
            self.expense_table.setCellWidget(i, 5, del_btn)

    def save_expense(self):
        title = self.title_input.text().strip()
        category = self.category_combo.currentText()
        amount = self.amount_input.value()
        date = self.date_input.date().toString("yyyy-MM-dd")
        desc = self.desc_input.text().strip()

        if not title or amount <= 0:
            QMessageBox.warning(self, "Validation Error", "Title and Amount are required")
            return

        try:
            self.db.add_expense(title, category, amount, desc, date)
            self.title_input.clear()
            self.amount_input.setValue(0)
            self.desc_input.clear()
            self.refresh_table()
            QMessageBox.information(self, "Success", "Expense saved successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save expense: {str(e)}")

    def delete_expense(self, expense_id):
        reply = QMessageBox.question(self, 'Confirm Delete', "Are you sure you want to delete this expense?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_expense(expense_id)
            self.refresh_table()
