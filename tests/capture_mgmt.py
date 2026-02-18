import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from src.database.db_manager import DatabaseManager
from src.ui.main_window import MainWindow

def capture_mgmt_screens():
    app = QApplication(sys.argv)
    db = DatabaseManager("test_mgmt.db")
    db.add_category("Drinks")
    db.add_menu_item(1, "Coffee", 2.50)
    db.add_table("T1", 2)

    # Load styles
    style_path = "src/ui/styles.qss"
    if os.path.exists(style_path):
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())

    user = {'username': 'admin', 'role': 'Admin', 'full_name': 'System Admin'}
    main = MainWindow(db, user)
    main.show()

    def take_screenshots():
        # Menu Page
        main.switch_page('menu')
        main.grab().save("menu_mgmt_screen.png")
        print("Menu screen captured.")

        # Table Page
        main.switch_page('tables')
        main.grab().save("table_mgmt_screen.png")
        print("Table screen captured.")

        app.quit()

    QTimer.singleShot(1000, take_screenshots)
    app.exec()
    if os.path.exists("test_mgmt.db"): os.remove("test_mgmt.db")

if __name__ == "__main__":
    capture_mgmt_screens()
