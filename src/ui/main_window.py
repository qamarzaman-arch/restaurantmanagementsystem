from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QStackedWidget, QLabel, QFrame)
from PyQt6.QtCore import Qt
from src.ui.menu_mgmt import MenuManagementScreen
from src.ui.table_mgmt import TableManagementScreen
from src.ui.order_screen import OrderScreen
from src.ui.dashboard import DashboardScreen
from src.ui.reports_screen import ReportsScreen

class MainWindow(QMainWindow):
    def __init__(self, db_manager, user):
        super().__init__()
        self.db = db_manager
        self.user = user
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Restaurant Management System")
        self.setMinimumSize(1000, 700)

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        user_info = QLabel(f"Welcome,\n{self.user['full_name']}")
        user_info.setStyleSheet("color: white; padding: 10px; font-weight: bold;")
        sidebar_layout.addWidget(user_info)

        sidebar_layout.addSpacing(20)

        self.nav_buttons = {}
        nav_items = [
            ("Dashboard", "dashboard"),
            ("Orders", "orders"),
            ("Menu Management", "menu"),
            ("Table Management", "tables"),
            ("Inventory", "inventory"),
            ("Reports", "reports"),
            ("Settings", "settings"),
        ]

        # Filter based on role if needed
        if self.user['role'] != 'Admin':
            nav_items = [i for i in nav_items if i[1] in ['dashboard', 'orders', 'tables']]

        for label, name in nav_items:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.clicked.connect(lambda checked, n=name: self.switch_page(n))
            sidebar_layout.addWidget(btn)
            self.nav_buttons[name] = btn

        sidebar_layout.addStretch()

        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.close) # For now just close
        sidebar_layout.addWidget(logout_btn)

        main_layout.addWidget(self.sidebar)

        # Content Area
        self.content_stack = QStackedWidget()

        # Pages
        self.pages = {}

        # Dashboard
        self.pages['dashboard'] = DashboardScreen(self.db)
        self.content_stack.addWidget(self.pages['dashboard'])

        # Menu Management
        self.pages['menu'] = MenuManagementScreen(self.db)
        self.content_stack.addWidget(self.pages['menu'])

        # Table Management
        self.pages['tables'] = TableManagementScreen(self.db)
        self.content_stack.addWidget(self.pages['tables'])

        # Order Screen
        self.pages['orders'] = OrderScreen(self.db)
        self.content_stack.addWidget(self.pages['orders'])

        # Reports Screen
        self.pages['reports'] = ReportsScreen(self.db)
        self.content_stack.addWidget(self.pages['reports'])

        # Other placeholders
        for name in ['inventory', 'settings']:
            if name not in self.pages:
                page = QWidget()
                layout = QVBoxLayout(page)
                layout.addWidget(QLabel(f"<h1>{name.capitalize()} Page</h1>"))
                self.content_stack.addWidget(page)
                self.pages[name] = page

        main_layout.addWidget(self.content_stack)

        self.setCentralWidget(main_widget)

        # Default page
        if nav_items:
            self.nav_buttons[nav_items[0][1]].setChecked(True)
            self.switch_page(nav_items[0][1])

    def switch_page(self, name):
        self.content_stack.setCurrentWidget(self.pages[name])
