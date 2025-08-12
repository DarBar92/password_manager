from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QTimer

class Toast(QLabel):
    def __init__(self, message, parent=None, duration=2000):
        super().__init__(parent)
        
        self.setText(message)
        self.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 180);
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 12px;
            }
        """)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.ToolTip
        )
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.adjustSize()

        if parent:
            parent_rect = parent.geometry()
            self.move(
                parent_rect.left() + parent_rect.width() - self.width() - 20,
                parent_rect.top() + parent_rect.height() - self.height() - 20
            )
        self.show()

        QTimer.singleShot(duration, self.close)
