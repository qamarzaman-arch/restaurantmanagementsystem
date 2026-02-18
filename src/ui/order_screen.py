from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QComboBox, QHeaderView, QMessageBox, QScrollArea,
                             QGridLayout, QFrame, QDoubleSpinBox)
from PyQt6.QtCore import Qt, pyqtSignal
from src.logic.billing import BillingLogic
from src.utils.pdf_generator import PDFGenerator
import datetime

class OrderScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.current_order_id = None
        self.cart_items = []
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)

        # Left side: Menu Browsing
        left_layout = QVBoxLayout()

        # Table Selection
        table_nav = QHBoxLayout()
        table_nav.addWidget(QLabel("Select Table:"))
        self.table_combo = QComboBox()
        self.refresh_tables()
        table_nav.addWidget(self.table_combo)

        self.start_order_btn = QPushButton("Start Order")
        self.start_order_btn.clicked.connect(self.start_order)
        table_nav.addWidget(self.start_order_btn)

        left_layout.addLayout(table_nav)

        # Categories
        self.cat_tabs = QHBoxLayout()
        self.refresh_category_buttons()
        left_layout.addLayout(self.cat_tabs)

        # Items Grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.items_container = QWidget()
        self.items_grid = QGridLayout(self.items_container)
        scroll.setWidget(self.items_container)
        left_layout.addWidget(scroll)

        layout.addLayout(left_layout, 2)

        # Right side: Cart and Billing
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("<b>Current Order</b>"))

        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(4)
        self.cart_table.setHorizontalHeaderLabels(["Item", "Qty", "Price", "Total"])
        self.cart_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        right_layout.addWidget(self.cart_table)

        billing_frame = QFrame()
        billing_frame.setFrameShape(QFrame.Shape.StyledPanel)
        bill_layout = QGridLayout(billing_frame)

        bill_layout.addWidget(QLabel("Subtotal:"), 0, 0)
        self.subtotal_label = QLabel("0.00")
        bill_layout.addWidget(self.subtotal_label, 0, 1)

        bill_layout.addWidget(QLabel("Discount (%):"), 1, 0)
        self.discount_input = QDoubleSpinBox()
        self.discount_input.valueChanged.connect(self.update_totals)
        bill_layout.addWidget(self.discount_input, 1, 1)

        bill_layout.addWidget(QLabel("Tax:"), 2, 0)
        self.tax_label = QLabel("0.00")
        bill_layout.addWidget(self.tax_label, 2, 1)

        bill_layout.addWidget(QLabel("<b>Total:</b>"), 3, 0)
        self.total_label = QLabel("<b>0.00</b>")
        bill_layout.addWidget(self.total_label, 3, 1)

        right_layout.addWidget(billing_frame)

        # Checkout
        pay_layout = QHBoxLayout()
        self.payment_method = QComboBox()
        self.payment_method.addItems(["Cash", "Card", "Online"])
        pay_layout.addWidget(QLabel("Payment:"))
        pay_layout.addWidget(self.payment_method)

        self.checkout_btn = QPushButton("Checkout & Print")
        self.checkout_btn.setObjectName("actionButton")
        self.checkout_btn.setEnabled(False)
        self.checkout_btn.clicked.connect(self.checkout)
        pay_layout.addWidget(self.checkout_btn)

        right_layout.addLayout(pay_layout)

        layout.addLayout(right_layout, 1)

        self.refresh_items()

    def refresh_tables(self):
        self.table_combo.clear()
        tables = self.db.get_tables()
        for t in tables:
            status = f" ({t['status']})" if t['status'] != 'Available' else ""
            self.table_combo.addItem(f"Table {t['table_number']}{status}", t['id'])

    def refresh_category_buttons(self):
        # Clear existing
        while self.cat_tabs.count():
            item = self.cat_tabs.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        cats = self.db.get_categories()
        all_btn = QPushButton("All")
        all_btn.clicked.connect(lambda: self.refresh_items(None))
        self.cat_tabs.addWidget(all_btn)

        for cat in cats:
            btn = QPushButton(cat['name'])
            btn.clicked.connect(lambda checked, c=cat['id']: self.refresh_items(c))
            self.cat_tabs.addWidget(btn)

    def refresh_items(self, cat_id=None):
        # Clear grid
        while self.items_grid.count():
            item = self.items_grid.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        items = self.db.get_menu_items(cat_id)
        for i, item in enumerate(items):
            btn = QPushButton(f"{item['name']}\n{item['price']:.2f}")
            btn.setFixedSize(120, 80)
            btn.clicked.connect(lambda checked, it=item: self.add_to_cart(it))
            self.items_grid.addWidget(btn, i // 4, i % 4)

    def start_order(self):
        table_id = self.table_combo.currentData()
        self.current_order_id = self.db.create_order(table_id, "Dine-in")
        self.cart_items = []
        self.refresh_cart_table()
        self.checkout_btn.setEnabled(True)
        self.start_order_btn.setEnabled(False)
        self.refresh_tables()

    def add_to_cart(self, item):
        if not self.current_order_id:
            QMessageBox.warning(self, "No Order", "Please start an order first")
            return

        # Check if item already in cart
        for cart_item in self.cart_items:
            if cart_item['id'] == item['id']:
                cart_item['quantity'] += 1
                self.refresh_cart_table()
                return

        self.cart_items.append({
            'id': item['id'],
            'name': item['name'],
            'price': item['price'],
            'quantity': 1
        })
        self.refresh_cart_table()

    def refresh_cart_table(self):
        self.cart_table.setRowCount(len(self.cart_items))
        for i, item in enumerate(self.cart_items):
            self.cart_table.setItem(i, 0, QTableWidgetItem(item['name']))
            self.cart_table.setItem(i, 1, QTableWidgetItem(str(item['quantity'])))
            self.cart_table.setItem(i, 2, QTableWidgetItem(f"{item['price']:.2f}"))
            self.cart_table.setItem(i, 3, QTableWidgetItem(f"{(item['price']*item['quantity']):.2f}"))
        self.update_totals()

    def update_totals(self):
        tax_rate = float(self.db.get_setting("tax_rate", 5.0))
        discount = self.discount_input.value()

        res = BillingLogic.calculate_totals(self.cart_items, tax_rate, discount)
        self.subtotal_label.setText(f"{res['subtotal']:.2f}")
        self.tax_label.setText(f"{res['tax']:.2f}")
        self.total_label.setText(f"<b>{res['total']:.2f}</b>")
        self.current_totals = res

    def checkout(self):
        if not self.cart_items:
            QMessageBox.warning(self, "Empty Cart", "Please add items to the cart")
            return

        try:
            # Save order items to DB
            for item in self.cart_items:
                self.db.add_order_item(self.current_order_id, item['id'], item['quantity'], item['price'])

            # Update order payment
            self.db.update_order_payment(
                self.current_order_id,
                self.current_totals['subtotal'],
                self.current_totals['tax'],
                self.current_totals['discount'],
                self.current_totals['total'],
                self.payment_method.currentText()
            )

            # Generate PDF
            order_data = self.db.get_order(self.current_order_id)
            settings = self.db.get_all_settings()
            filename = f"invoices/invoice_{self.current_order_id}.pdf"
            os.makedirs("invoices", exist_ok=True)
            try:
                PDFGenerator.generate_invoice(order_data, settings, filename)
                pdf_msg = f"\nInvoice saved to {filename}"
            except Exception as pdf_err:
                pdf_msg = f"\nWarning: Could not generate PDF: {str(pdf_err)}"

            QMessageBox.information(self, "Success", f"Order completed!{pdf_msg}")

            # Reset
            self.current_order_id = None
            self.cart_items = []
            self.refresh_cart_table()
            self.refresh_tables()
            self.checkout_btn.setEnabled(False)
            self.start_order_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Checkout Error", f"An error occurred during checkout: {str(e)}")
