import sys
import os
import json
from PyQt6.QtWidgets import (
    QApplication,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QLineEdit,
    QHeaderView,
    QMessageBox,
    QMenu,
    QDialog,
)
from PyQt6.QtCore import Qt 
from PyQt6.QtGui import QIcon, QAction
from master_password_dialog import MasterPasswordDialog
from crypto_utils import encrypt_data, decrypt_data, derive_key
from toast import Toast
from add_entry_dialog import AddEntryDialog

DATA_FILE = "passwords.dat"

class PasswordManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Manager")
        self.setGeometry(100, 100, 500, 400)

        # --- Prompt for correct master password in a loop ---
        self.encryption_key = None
        self.entries = []

        while True:
            dialog = MasterPasswordDialog()
            if dialog.exec() != QDialog.DialogCode.Accepted:
                sys.exit()

            password = dialog.get_password()
            key = derive_key(password)

            try:
                self.entries = self.load_entries_from_file(key)
                self.encryption_key = key
                break  # ✅ Success: valid password
            except Exception:
                QMessageBox.warning(None, "Incorrect Password", "Master password is incorrect or data is corrupted. Please try again.")

        # --- GUI Layout ---
        self.layout = QVBoxLayout()

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Website", "Username", "Password"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_context_menu)


        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by website or username...")
        self.search_bar.textChanged.connect(self.filter_entries)

        search_icon_action = QAction(QIcon.fromTheme("edit-find"), "Edit", self.search_bar)
        self.search_bar.addAction(search_icon_action, QLineEdit.ActionPosition.LeadingPosition)

        self.clear_action = QAction(QIcon.fromTheme("edit-clear"), "Clear", self.search_bar)
        self.clear_action.triggered.connect(self.clear_search)
        self.search_bar.addAction(self.clear_action, QLineEdit.ActionPosition.TrailingPosition)
        self.clear_action.setVisible(False)

        self.search_bar.textChanged.connect(self.toggle_clear_button)

        self.show_passwords = False

        self.show_passwords_button = QPushButton("Show Passwords")
        self.show_passwords_button.clicked.connect(self.toggle_password_visibility)

        self.add_button = QPushButton("Add Entry")
        self.add_button.clicked.connect(self.add_entry)

        self.edit_button = QPushButton("Edit Entry")
        self.edit_button.clicked.connect(self.edit_entry)

        self.delete_button = QPushButton("Delete Entry")
        self.delete_button.clicked.connect(self.delete_entry)

        button_row = QHBoxLayout()
        button_row.addWidget(self.add_button)
        button_row.addWidget(self.edit_button)
        button_row.addWidget(self.delete_button)

        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.show_passwords_button)
        self.layout.addWidget(self.table)
        self.layout.addLayout(button_row)
        self.setLayout(self.layout)

        # Populate table with entries
        for entry in self.entries:
            self.insert_entry_into_table(entry)

    def clear_search(self):
        self.search_bar.clear()
        self.filter_entries()

    def toggle_clear_button(self, text):
        self.clear_action.setVisible(bool(text.strip()))

    def filter_entries(self):
        query = self.search_bar.text().lower()

        self.table.setRowCount(0)  # Clear current table

        for entry in self.entries:
            if query in entry["website"].lower() or query in entry["username"].lower():
                self.insert_entry_into_table(entry)


    def toggle_password_visibility(self):
        self.show_passwords = not self.show_passwords
        self.show_passwords_button.setText("Hide Passwords" if self.show_passwords else "Show Passwords")
        self.refresh_table_passwords()

    def refresh_table_passwords(self):
        for row, entry in enumerate(self.entries):
            password = entry["password"]
            display_text = password if self.show_passwords else "•••••"
            self.table.setItem(row, 2, QTableWidgetItem(display_text))

    def copy_username(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select an entry to copy the username.")
            return
        
        username = self.entries[selected_row]["username"]
        QApplication.clipboard().setText(username)
        Toast("Username copied!", self)

    def copy_password(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select an entry to copy the password.")
            return
        
        password = self.entries[selected_row]["password"]
        QApplication.clipboard().setText(password)
        Toast("Password copied!", self)

    def add_entry(self):
        dialog = AddEntryDialog()
        if dialog.exec():
            entry = dialog.get_data()
            self.entries.append(entry)
            self.insert_entry_into_table(entry)
            self.filter_entries()
        else:
            print("Entry addition cancelled.")
    
    def edit_entry(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select an entry to edit.")
            return
        
        current_entry = self.entries[selected_row]

        dialog = AddEntryDialog()
        dialog.website_input.setText(current_entry["website"])
        dialog.username_input.setText(current_entry["username"])
        dialog.password_input.setText(current_entry["password"])

        if dialog.exec():
            updated_entry = dialog.get_data()
            self.entries[selected_row] = updated_entry
            self.table.setItem(selected_row, 0, QTableWidgetItem(updated_entry["website"]))
            self.table.setItem(selected_row, 1, QTableWidgetItem(updated_entry["username"]))
            self.table.setItem(selected_row, 2, QTableWidgetItem(updated_entry["password"]))
            self.refresh_table_passwords()
            self.filter_entries()

    def delete_entry(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select an entry to delete.")
            return
        
        confirm = QMessageBox.question(
            self,
            "Delete Entry",
            "Are you sure you want to delete this entry?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            self.entries.pop(selected_row)
            self.table.removeRow(selected_row)
            self.filter_entries()

    def insert_entry_into_table(self, entry):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(entry["website"]))
        self.table.setItem(row_position, 1, QTableWidgetItem(entry["username"]))
        password_display = entry["password"] if self.show_passwords else "•••••"
        self.table.setItem(row_position, 2, QTableWidgetItem(password_display))
    
    def save_entries_to_file(self):
        try:
            data_str = json.dumps(self.entries)
            encrypted = encrypt_data(data_str, self.encryption_key)
            with open(DATA_FILE, "wb") as f:
                f.write(encrypted)
            print("Entries saved securely.")
        except Exception as e:
            print(f"Error saving entries: {e}")

    def load_entries_from_file(self, key):
        if not os.path.exists(DATA_FILE):
            return []

        with open(DATA_FILE, "rb") as f:
            encrypted = f.read()

        decrypted_str = decrypt_data(encrypted, key)  # <- raises exception if wrong key
        return json.loads(decrypted_str)

    def closeEvent(self, event):
        self.save_entries_to_file()
        event.accept()

    def open_context_menu(self, position):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return
        
        menu = QMenu(self)

        copy_username_action = menu.addAction("Copy Username")
        copy_password_action = menu.addAction("Copy Password")
        edit_action = menu.addAction("Edit Entry")
        delete_action = menu.addAction("Delete Entry")

        action = menu.exec(self.table.viewport().mapToGlobal(position))

        if action == copy_username_action:
            self.copy_username()
        elif action == copy_password_action:
            self.copy_password()
        elif action == edit_action:
            self.edit_entry()
        elif action == delete_action:
            self.delete_entry()