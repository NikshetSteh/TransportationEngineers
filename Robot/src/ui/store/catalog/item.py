from PySide6.QtWidgets import QWidget

from ui.store.catalog.item_ui import Ui_ItemUI as Design


class Item(QWidget):
    def __init__(self, parent=None):
        super(Item, self).__init__(parent)
        self.ui = Design()
        self.ui.setupUi(self)
        self.setMinimumSize(450, 155)
