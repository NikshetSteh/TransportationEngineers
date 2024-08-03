from PySide6 import QtWidgets
from PySide6.QtGui import QFont, QPixmap, Qt
from PySide6.QtWidgets import QLabel, QWidget


class ItemInfoUI:
    def __init__(self):
        self.description_label = None
        self.icon_label = None
        self.name_label = None

    def setup_ui(
            self,
            widget: QWidget,
            base_width: int,
            margins: int,
            nane: str,
            description: str,
            image: QPixmap
    ) -> "ItemInfoUI":
        elements_width = base_width - margins * 2

        name_font = QFont()
        name_font.setFamilies([u"Rubik"])
        name_font.setPointSize(12)
        name_font.setBold(True)

        self.name_label = QLabel(widget)
        self.name_label.setGeometry(margins, margins, elements_width, 32)
        self.name_label.setTextFormat(Qt.TextFormat.AutoText)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setWordWrap(True)
        self.name_label.setText(nane)
        self.name_label.setFont(name_font)

        self.icon_label = QLabel(widget)
        self.icon_label.setGeometry(margins, margins * 2 + 32, elements_width, 200)
        self.icon_label.setPixmap(image)
        self.icon_label.setScaledContents(True)

        self.description_label = QLabel(widget)
        self.description_label.setGeometry(margins, margins * 3 + 32 + 200, elements_width, 200)
        self.description_label.setTextFormat(Qt.TextFormat.AutoText)
        self.description_label.setWordWrap(True)
        self.description_label.setText(description)
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        self.description_label.setSizePolicy(size_policy)
        self.description_label.setFixedWidth(elements_width)
        self.description_label.adjustSize()

        rect = self.description_label.geometry()

        widget.setMinimumSize(elements_width, margins * 4 + 32 + 200 + rect.height())

        return self
