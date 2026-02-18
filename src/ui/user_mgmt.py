from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QComboBox, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt

class UserManagementScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.editing_user_id = None
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)

        # Left side: Form
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        form_layout.addWidget(QLabel("<b>Add/Edit User</b>"))

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        form_layout.addWidget(QLabel("Username"))
        form_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(QLabel("Password"))
        form_layout.addWidget(self.password_input)

        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Full Name")
        form_layout.addWidget(QLabel("Full Name"))
        form_layout.addWidget(self.fullname_input)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["Admin", "Staff"])
        form_layout.addWidget(QLabel("Role"))
        form_layout.addWidget(self.role_combo)

        self.save_btn = QPushButton("Add User")
        self.save_btn.setObjectName("actionButton")
        self.save_btn.clicked.connect(self.save_user)
        form_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("Cancel Edit")
        self.cancel_btn.setVisible(False)
        self.cancel_btn.clicked.connect(self.clear_form)
        form_layout.addWidget(self.cancel_btn)

        layout.addLayout(form_layout, 1)

        # Right side: Table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(["ID", "Username", "Role", "Action"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.user_table, 2)

        self.refresh_table()

    def refresh_table(self):
        users = self.db.get_users()
        self.user_table.setRowCount(len(users))
        for i, user in enumerate(users):
            self.user_table.setItem(i, 0, QTableWidgetItem(str(user['id'])))
            self.user_table.setItem(i, 1, QTableWidgetItem(user['username']))
            self.user_table.setItem(i, 2, QTableWidgetItem(user['role']))

            action_layout = QHBoxLayout()
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, u=user: self.edit_user(u))

            del_btn = QPushButton("Delete")
            del_btn.setObjectName("dangerButton")
            del_btn.clicked.connect(lambda checked, uid=user['id']: self.delete_user(uid))

            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(2, 2, 2, 2)
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(del_btn)

            self.user_table.setCellWidget(i, 3, action_widget)

    def edit_user(self, user):
        self.editing_user_id = user['id']
        self.username_input.setText(user['username'])
        self.fullname_input.setText(user['full_name'] or "")
        self.role_combo.setCurrentText(user['role'])
        self.password_input.setPlaceholderText("Leave blank to keep current")
        self.save_btn.setText("Update User")
        self.cancel_btn.setVisible(True)

    def clear_form(self):
        self.editing_user_id = None
        self.username_input.clear()
        self.password_input.clear()
        self.password_input.setPlaceholderText("Password")
        self.fullname_input.clear()
        self.save_btn.setText("Add User")
        self.cancel_btn.setVisible(False)

    def save_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_combo.currentText()
        fullname = self.fullname_input.text().strip()

        if not username:
            QMessageBox.warning(self, "Validation Error", "Username is required")
            return

        if self.editing_user_id:
            data = {'username': username, 'role': role, 'full_name': fullname}
            if password:
                data['password'] = password
            self.db.update_user(self.editing_user_id, **data)
            QMessageBox.information(self, "Success", "User updated successfully")
            self.clear_form()
            self.refresh_table()
        else:
            if not password:
                QMessageBox.warning(self, "Validation Error", "Password is required for new user")
                return
            if self.db.add_user(username, password, role, fullname):
                self.clear_form()
                self.refresh_table()
                QMessageBox.information(self, "Success", "User added successfully")
            else:
                QMessageBox.warning(self, "Error", "Username already exists")

    def delete_user(self, user_id):
        reply = QMessageBox.question(self, 'Confirm Delete', "Are you sure you want to delete this user?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_user(user_id)
            self.refresh_table()
