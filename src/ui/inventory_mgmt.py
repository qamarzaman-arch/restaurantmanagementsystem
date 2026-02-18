from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QDoubleSpinBox, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class InventoryManagementScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)

        # Left side: Form
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        form_layout.addWidget(QLabel("<b>Add/Update Inventory</b>"))

        self.item_name = QLineEdit()
        self.item_name.setPlaceholderText("Item Name (e.g. Potato)")
        form_layout.addWidget(QLabel("Item Name"))
        form_layout.addWidget(self.item_name)

        self.quantity = QDoubleSpinBox()
        self.quantity.setRange(-10000, 10000)
        form_layout.addWidget(QLabel("Quantity to Add/Update"))
        form_layout.addWidget(self.quantity)

        self.unit = QLineEdit()
        self.unit.setPlaceholderText("Unit (e.g. kg, pcs)")
        form_layout.addWidget(QLabel("Unit"))
        form_layout.addWidget(self.unit)

        self.threshold = QDoubleSpinBox()
        self.threshold.setRange(0, 1000)
        form_layout.addWidget(QLabel("Min Threshold (Alert)"))
        form_layout.addWidget(self.threshold)

        save_btn = QPushButton("Save Inventory Item")
        save_btn.setObjectName("actionButton")
        save_btn.clicked.connect(self.save_inventory)
        form_layout.addWidget(save_btn)

        layout.addLayout(form_layout, 1)

        # Right side: Inventory List
        right_layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search inventory...")
        self.search_input.textChanged.connect(self.refresh_table)
        search_layout.addWidget(self.search_input)
        right_layout.addLayout(search_layout)

        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(6)
        self.inventory_table.setHorizontalHeaderLabels(["ID", "Item", "Qty", "Unit", "Status", "Action"])
        self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        right_layout.addWidget(self.inventory_table)

        layout.addLayout(right_layout, 2)

        self.refresh_table()

    def refresh_table(self):
        self.inventory_table.setRowCount(0)
        search_text = self.search_input.text().lower()
        items = self.db.get_inventory()

        # Filter items
        filtered_items = [i for i in items if search_text in i['item_name'].lower()]

        self.inventory_table.setRowCount(len(filtered_items))
        for i, item in enumerate(filtered_items):
            # ID
            self.inventory_table.setItem(i, 0, QTableWidgetItem(str(item['id'])))
            # Item Name
            self.inventory_table.setItem(i, 1, QTableWidgetItem(item['item_name']))
            # Quantity
            self.inventory_table.setItem(i, 2, QTableWidgetItem(f"{item['quantity']:.2f}"))
            # Unit
            self.inventory_table.setItem(i, 3, QTableWidgetItem(item['unit']))

            # Status
            status = "OK"
            color = "#10ac84"
            if item['quantity'] <= item['min_threshold']:
                status = "LOW"
                color = "#ee5253"

            status_item = QTableWidgetItem(status)
            status_item.setForeground(QColor("white"))
            status_item.setBackground(QColor(color))
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.inventory_table.setItem(i, 4, status_item)

            # Action
            del_btn = QPushButton("Delete")
            del_btn.setObjectName("dangerButton")
            del_btn.clicked.connect(lambda checked, iid=item['id']: self.delete_item(iid))
            self.inventory_table.setCellWidget(i, 5, del_btn)

    def delete_item(self, item_id):
        reply = QMessageBox.question(self, 'Confirm Delete', "Delete this inventory item?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_inventory_item(item_id)
            self.refresh_table()

    def save_inventory(self):
        name = self.item_name.text().strip()
        qty = self.quantity.value()
        unit = self.unit.text().strip()
        thresh = self.threshold.value()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Item name is required")
            return

        try:
            self.db.update_inventory(name, qty, unit)
            # Threshold update needs a direct SQL if not in update_inventory
            with self.db.get_connection() as conn:
                conn.execute("UPDATE inventory SET min_threshold = ? WHERE item_name = ?", (thresh, name))

            self.item_name.clear()
            self.quantity.setValue(0)
            self.unit.clear()
            self.threshold.setValue(0)
            self.refresh_table()
            QMessageBox.information(self, "Success", "Inventory updated")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update inventory: {str(e)}")
