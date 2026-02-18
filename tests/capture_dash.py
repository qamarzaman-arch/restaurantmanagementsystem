import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from src.database.db_manager import DatabaseManager
from src.ui.main_window import MainWindow

def capture_dashboard():
    app = QApplication(sys.argv)
    db = DatabaseManager("test_dash.db")

    # Add some dummy data
    db.add_category("Food")
    db.add_menu_item(1, "Pizza", 10.0)
    db.add_table("T1", 4)
    oid = db.create_order(1, "Dine-in")
    db.add_order_item(oid, 1, 2, 10.0)
    db.update_order_payment(oid, 20.0, 1.0, 0, 21.0, "Cash")

    # Load styles
    style_path = "src/ui/styles.qss"
    if os.path.exists(style_path):
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())

    user = {'username': 'admin', 'role': 'Admin', 'full_name': 'System Admin'}
    main = MainWindow(db, user)
    main.show()

    def check_dash():
        main.switch_page('dashboard')
        main.grab().save("dashboard_screen.png")
        print("Dashboard screen captured.")

        # Test report export
        main.switch_page('reports')
        main.pages['reports'].export_csv()
        print("CSV export tested.")

        app.quit()

    QTimer.singleShot(1000, check_dash)
    app.exec()
    if os.path.exists("test_dash.db"): os.remove("test_dash.db")

if __name__ == "__main__":
    capture_dashboard()
