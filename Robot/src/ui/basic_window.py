from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow


class BasicWindow(QMainWindow):
    def __init__(self):
        super(BasicWindow, self).__init__()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.is_active = True

        self.resize(1080, 600)
