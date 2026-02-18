from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFileDialog, QMessageBox, QFrame, QComboBox, QScrollArea)
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

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        form_frame = QFrame()
        form_frame.setObjectName("settingsFrame")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(10)

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

        # Backup & Restore
        form_layout.addWidget(QLabel("Database Management"))
        db_mgmt_layout = QHBoxLayout()
        backup_btn = QPushButton("Backup Database")
        backup_btn.clicked.connect(self.backup_db)
        db_mgmt_layout.addWidget(backup_btn)

        restore_btn = QPushButton("Restore Database")
        restore_btn.setObjectName("dangerButton")
        restore_btn.clicked.connect(self.restore_db)
        db_mgmt_layout.addWidget(restore_btn)
        form_layout.addLayout(db_mgmt_layout)

        save_btn = QPushButton("Save Settings")
        save_btn.setObjectName("actionButton")
        save_btn.setMinimumHeight(40)
        save_btn.clicked.connect(self.save_settings)
        form_layout.addWidget(save_btn)

        scroll_layout.addWidget(form_frame)
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

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

    def backup_db(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Backup Database", "", "Database Files (*.db)")
        if file_path:
            if self.db.backup_database(file_path):
                QMessageBox.information(self, "Success", f"Database backed up to {file_path}")
            else:
                QMessageBox.critical(self, "Error", "Failed to backup database")

    def restore_db(self):
        reply = QMessageBox.question(self, 'Confirm Restore',
                                   "Restoring will overwrite current data. Are you sure?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            file_path, _ = QFileDialog.getOpenFileName(self, "Restore Database", "", "Database Files (*.db)")
            if file_path:
                if self.db.restore_database(file_path):
                    QMessageBox.information(self, "Success", "Database restored. Please restart the application.")
                else:
                    QMessageBox.critical(self, "Error", "Failed to restore database")
