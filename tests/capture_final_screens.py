import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from src.database.db_manager import DatabaseManager
from src.ui.main_window import MainWindow

def capture_all():
    app = QApplication(sys.argv)

    # Load Styles
    style_path = "src/ui/styles.qss"
    if os.path.exists(style_path):
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())

    db = DatabaseManager("test_final.db")

    # Setup some test data
    db.add_category("Food")
    db.add_menu_item(1, "Burger", 10.0, "Delicious")
    db.update_inventory("Potato", 2, "kg") # Low stock
    with db.get_connection() as conn:
        conn.execute("UPDATE inventory SET min_threshold = 5 WHERE item_name = 'Potato'")

    user = {'id': 1, 'username': 'admin', 'role': 'Admin', 'full_name': 'Admin User'}
    main = MainWindow(db, user)
    main.show()

    os.makedirs("final_verification", exist_ok=True)

    def step1():
        main.switch_page('dashboard')
        main.grab().save("final_verification/dashboard_final.png")
        print("Captured Dashboard")

    def step2():
        main.switch_page('inventory')
        main.grab().save("final_verification/inventory_final.png")
        print("Captured Inventory")

    def step3():
        main.switch_page('orders')
        main.grab().save("final_verification/orders_final.png")
        print("Captured Orders")

    def step4():
        main.switch_page('settings')
        main.grab().save("final_verification/settings_final.png")
        print("Captured Settings")
        app.quit()

    QTimer.singleShot(500, step1)
    QTimer.singleShot(1000, step2)
    QTimer.singleShot(1500, step3)
    QTimer.singleShot(2000, step4)

    sys.exit(app.exec())

if __name__ == "__main__":
    # Headless mode
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    capture_all()
