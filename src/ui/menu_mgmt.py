from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QComboBox, QDoubleSpinBox, QHeaderView, QMessageBox, QTabWidget)
from PyQt6.QtCore import Qt

class MenuManagementScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.init_items_tab()
        self.init_categories_tab()

        layout.addWidget(self.tabs)

    def init_items_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)

        # Left side: Form
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        form_layout.addWidget(QLabel("<b>Add/Edit Menu Item</b>"))

        self.item_name = QLineEdit()
        self.item_name.setPlaceholderText("Item Name")
        form_layout.addWidget(QLabel("Name"))
        form_layout.addWidget(self.item_name)

        self.item_cat = QComboBox()
        self.refresh_categories_combo()
        form_layout.addWidget(QLabel("Category"))
        form_layout.addWidget(self.item_cat)

        self.item_price = QDoubleSpinBox()
        self.item_price.setMaximum(10000)
        form_layout.addWidget(QLabel("Price"))
        form_layout.addWidget(self.item_price)

        self.item_desc = QLineEdit()
        self.item_desc.setPlaceholderText("Description")
        form_layout.addWidget(QLabel("Description"))
        form_layout.addWidget(self.item_desc)

        add_btn = QPushButton("Save Item")
        add_btn.setObjectName("actionButton")
        add_btn.clicked.connect(self.save_item)
        form_layout.addWidget(add_btn)

        layout.addLayout(form_layout, 1)

        # Right side: Table
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(5)
        self.items_table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Price", "Action"])
        self.items_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.items_table, 3)

        self.tabs.addTab(tab, "Menu Items")
        self.refresh_items_table()

    def init_categories_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)

        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        form_layout.addWidget(QLabel("<b>Add Category</b>"))

        self.cat_name = QLineEdit()
        form_layout.addWidget(self.cat_name)

        add_cat_btn = QPushButton("Add Category")
        add_cat_btn.clicked.connect(self.add_category)
        form_layout.addWidget(add_cat_btn)
        layout.addLayout(form_layout, 1)

        self.cats_table = QTableWidget()
        self.cats_table.setColumnCount(2)
        self.cats_table.setHorizontalHeaderLabels(["ID", "Name"])
        self.cats_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.cats_table, 2)

        self.tabs.addTab(tab, "Categories")
        self.refresh_categories_table()

    def refresh_categories_combo(self):
        self.item_cat.clear()
        cats = self.db.get_categories()
        for cat in cats:
            self.item_cat.addItem(cat['name'], cat['id'])

    def refresh_items_table(self):
        items = self.db.get_menu_items()
        self.items_table.setRowCount(len(items))
        for i, item in enumerate(items):
            self.items_table.setItem(i, 0, QTableWidgetItem(str(item['id'])))
            self.items_table.setItem(i, 1, QTableWidgetItem(item['name']))
            self.items_table.setItem(i, 2, QTableWidgetItem(item['category_name']))
            self.items_table.setItem(i, 3, QTableWidgetItem(f"{item['price']:.2f}"))

            del_btn = QPushButton("Delete")
            del_btn.setObjectName("dangerButton")
            del_btn.clicked.connect(lambda checked, id=item['id']: self.delete_item(id))
            self.items_table.setCellWidget(i, 4, del_btn)

    def refresh_categories_table(self):
        cats = self.db.get_categories()
        self.cats_table.setRowCount(len(cats))
        for i, cat in enumerate(cats):
            self.cats_table.setItem(i, 0, QTableWidgetItem(str(cat['id'])))
            self.cats_table.setItem(i, 1, QTableWidgetItem(cat['name']))

    def add_category(self):
        name = self.cat_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation Error", "Category name cannot be empty")
            return

        try:
            if self.db.add_category(name):
                self.cat_name.clear()
                self.refresh_categories_table()
                self.refresh_categories_combo()
            else:
                QMessageBox.warning(self, "Error", f"Category '{name}' already exists")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to add category: {str(e)}")

    def save_item(self):
        name = self.item_name.text().strip()
        cat_id = self.item_cat.currentData()
        price = self.item_price.value()
        desc = self.item_desc.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Item name cannot be empty")
            return
        if not cat_id:
            QMessageBox.warning(self, "Validation Error", "Please select a category")
            return
        if price <= 0:
            QMessageBox.warning(self, "Validation Error", "Price must be greater than zero")
            return

        try:
            self.db.add_menu_item(cat_id, name, price, desc)
            self.item_name.clear()
            self.item_price.setValue(0)
            self.item_desc.clear()
            self.refresh_items_table()
            QMessageBox.information(self, "Success", "Menu item saved successfully")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save menu item: {str(e)}")

    def delete_item(self, item_id):
        reply = QMessageBox.question(self, 'Confirm Delete',
                                   "Are you sure you want to delete this item?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_menu_item(item_id)
                self.refresh_items_table()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Failed to delete item: {str(e)}")
