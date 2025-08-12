from PyQt6.QtWidgets import(
QDialog, 
QVBoxLayout, 
QFormLayout, 
QLineEdit, 
QPushButton, 
QMessageBox, 
QHBoxLayout
) 

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