import sys
import os
from PyQt6.QtWidgets import QApplication
from src.database.db_manager import DatabaseManager
from src.ui.login_window import LoginWindow
from src.ui.main_window import MainWindow

class RestaurantApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.db = DatabaseManager("restaurant.db")

        # Load Styles
        self.load_styles()

        self.login_window = LoginWindow(self.db)
        self.login_window.login_success.connect(self.show_main_window)
        self.login_window.show()

    def load_styles(self):
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
