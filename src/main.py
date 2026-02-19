import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from src.database.db_manager import DatabaseManager
from src.ui.login_window import LoginWindow
from src.ui.main_window import MainWindow

class RestaurantApp:
    def __init__(self):
        # High DPI support for Qt6
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        self.app = QApplication(sys.argv)

        # Set a default font to avoid "Point size <= 0" warnings on some systems
        default_font = QFont("Segoe UI", 10)
        self.app.setFont(default_font)

        self.db = DatabaseManager("restaurant.db")

        # Load Styles
        self.load_styles()

        self.login_window = LoginWindow(self.db)
        self.login_window.login_success.connect(self.show_main_window)
        self.login_window.show()

    def load_styles(self):
        # Handle path for PyInstaller bundle
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
            style_path = os.path.join(base_path, "src", "ui", "styles.qss")
        else:
            # When running from source, styles are relative to this file
            style_path = os.path.join(os.path.dirname(__file__), "ui", "styles.qss")
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.app.setStyleSheet(f.read())

    def show_main_window(self, user):
        self.main_window = MainWindow(self.db, user)
        self.main_window.show()
        self.login_window.close()

    def run(self):
        return self.app.exec()

if __name__ == "__main__":
    app = RestaurantApp()
    sys.exit(app.run())
