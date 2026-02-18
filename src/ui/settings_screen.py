from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFileDialog, QMessageBox, QFrame, QComboBox)
from PyQt6.QtCore import Qt
from src.utils.printer_utils import PrinterUtils
import os

class SettingsScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(QLabel("<h1 style='color: #2c3e50;'>Restaurant Settings</h1>"))

        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 20px; border: 1px solid #dcdde1;")
        form_layout = QVBoxLayout(form_frame)

        # Restaurant Name
        self.name_input = QLineEdit()
        self.name_input.setText(self.db.get_setting("restaurant_name", ""))
        form_layout.addWidget(QLabel("Restaurant Name"))
        form_layout.addWidget(self.name_input)

        # Address
        self.address_input = QLineEdit()
        self.address_input.setText(self.db.get_setting("address", ""))
        form_layout.addWidget(QLabel("Address"))
        form_layout.addWidget(self.address_input)

        # Tax Rate
        self.tax_input = QLineEdit()
        self.tax_input.setText(self.db.get_setting("tax_rate", "5.0"))
        form_layout.addWidget(QLabel("Tax Rate (%)"))
        form_layout.addWidget(self.tax_input)

        # Logo Path
        logo_layout = QHBoxLayout()
        self.logo_path_label = QLabel(self.db.get_setting("logo_path", "No logo selected"))
        self.logo_path_label.setStyleSheet("color: #7f8c8d;")
        logo_btn = QPushButton("Select Logo")
        logo_btn.clicked.connect(self.select_logo)
        logo_layout.addWidget(self.logo_path_label)
        logo_layout.addWidget(logo_btn)

        form_layout.addWidget(QLabel("Invoice Logo"))
        form_layout.addLayout(logo_layout)

        # Printer Config
        self.printer_combo = QComboBox()
        printers = PrinterUtils.get_available_printers()
        self.printer_combo.addItem("Default")
        self.printer_combo.addItems(printers)

        saved_printer = self.db.get_setting("printer_name", "Default")
        index = self.printer_combo.findText(saved_printer)
        if index >= 0:
            self.printer_combo.setCurrentIndex(index)

        form_layout.addWidget(QLabel("Thermal Printer Name"))
        form_layout.addWidget(self.printer_combo)

        save_btn = QPushButton("Save Settings")
        save_btn.setObjectName("actionButton")
        save_btn.clicked.connect(self.save_settings)
        form_layout.addWidget(save_btn)

        layout.addWidget(form_frame)
        layout.addStretch()

    def select_logo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Logo", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.logo_path_label.setText(file_path)

    def save_settings(self):
        try:
            self.db.set_setting("restaurant_name", self.name_input.text())
            self.db.set_setting("address", self.address_input.text())
            self.db.set_setting("tax_rate", self.tax_input.text())
            self.db.set_setting("logo_path", self.logo_path_label.text())
            self.db.set_setting("printer_name", self.printer_combo.currentText())
            QMessageBox.information(self, "Success", "Settings saved successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")
