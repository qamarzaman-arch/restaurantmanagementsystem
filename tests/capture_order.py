import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from src.database.db_manager import DatabaseManager
from src.ui.main_window import MainWindow

def capture_order_screen():
    app = QApplication(sys.argv)
    db = DatabaseManager("test_order.db")
    db.add_category("Main Course")
    db.add_menu_item(1, "Steak", 25.00)
    db.add_menu_item(1, "Pasta", 15.00)
    db.add_table("T1", 4)
    db.add_table("T2", 2)

    # Load styles
    style_path = "src/ui/styles.qss"
    if os.path.exists(style_path):
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())

    user = {'username': 'admin', 'role': 'Admin', 'full_name': 'System Admin'}
    main = MainWindow(db, user)
    main.show()

    def simulate_order():
        main.switch_page('orders')
        order_page = main.pages['orders']

        # Select table and start order
        order_page.table_combo.setCurrentIndex(0)
        order_page.start_order()

        # Add item
        order_page.add_to_cart({'id': 1, 'name': 'Steak', 'price': 25.00})

        main.grab().save("order_screen.png")
        print("Order screen captured.")
        app.quit()

    QTimer.singleShot(1000, simulate_order)
    app.exec()
    if os.path.exists("test_order.db"): os.remove("test_order.db")

if __name__ == "__main__":
    capture_order_screen()
