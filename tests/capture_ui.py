import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from src.database.db_manager import DatabaseManager
from src.ui.login_window import LoginWindow
from src.ui.main_window import MainWindow

def capture_login_screen():
    app = QApplication(sys.argv)
    db = DatabaseManager("test_ui.db")

    # Load styles
    style_path = "src/ui/styles.qss"
    if os.path.exists(style_path):
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())

    login = LoginWindow(db)
    login.show()

    def take_screenshot():
        pixmap = login.grab()
        pixmap.save("login_screen.png")
        print("Login screen captured.")
        app.quit()

    QTimer.singleShot(1000, take_screenshot)
    app.exec()
    if os.path.exists("test_ui.db"): os.remove("test_ui.db")

def capture_main_screen():
    app = QApplication(sys.argv)
    db = DatabaseManager("test_ui_main.db")

    # Load styles
    style_path = "src/ui/styles.qss"
    if os.path.exists(style_path):
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())

    user = {'username': 'admin', 'role': 'Admin', 'full_name': 'System Admin'}
    main = MainWindow(db, user)
    main.show()

    def take_screenshot():
        pixmap = main.grab()
        pixmap.save("main_screen.png")
        print("Main screen captured.")
        app.quit()

    QTimer.singleShot(1000, take_screenshot)
    app.exec()
    if os.path.exists("test_ui_main.db"): os.remove("test_ui_main.db")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "main":
        capture_main_screen()
    else:
        capture_login_screen()
