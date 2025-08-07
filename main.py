import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QDialog,
    QLineEdit,
    QFormLayout,
    QMessageBox
)
from PyQt6.QtCore import Qt

class AddEntryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add new Password Entry")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.website_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addRow("Website:", self.website_input)
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)

        layout.addLayout(form_layout)

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.handle_save)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def handle_save(self):
        website = self.website_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not website or not username or not password:
            QMessageBox.warning(self, "Input Error", "All fields must be filled out.")
            return

        self.accept()

    def get_data(self):
        return {
            "website": self.website_input.text(),
            "username": self.username_input.text(),
            "password": self.password_input.text()
        }

class PasswordManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Manager")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel("Your Saved Passwords will appear here.")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.add_button = QPushButton("Add Entry")
        self.add_button.clicked.connect(self.add_entry)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.add_button)
        self.setLayout(self.layout)

    def add_entry(self):
        dialog = AddEntryDialog()
        if dialog.exec():
            entry = dialog.get_data()
            print("new entry added:", entry) # For now just print to console
        else:
            print("Entry addition cancelled.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordManager()
    window.show()
    sys.exit(app.exec())