import sys
from PyQt6.QtWidgets import QApplication
from password_manager import PasswordManager

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordManager()
    window.show()
    sys.exit(app.exec())