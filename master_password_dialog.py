from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)

class MasterPasswordDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Master Password")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.label = QLabel("Enter Your Master Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.submit_button = QPushButton("Unlock")
        self.submit_button.clicked.connect(self.accept)

        layout.addWidget(self.label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
    
    def get_password(self):
        return self.password_input.text()