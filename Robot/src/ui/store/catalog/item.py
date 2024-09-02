from PySide6.QtWidgets import QWidget

from ui.store.catalog.item_ui import Ui_ItemUI as Design


class Item(QWidget):
    def __init__(self, name: str = "", price_penny: int = 0, parent=None):
        super(Item, self).__init__(parent)
        self.ui = Design()
        self.ui.setupUi(self)
        self.setMinimumSize(450, 155)
        self.ui.name.setText(name)
        if price_penny % 100 == 0:
            self.ui.price.setText(f"{price_penny // 100} руб.")
        else:
            self.ui.price.setText(f"{price_penny // 100}.{price_penny % 100} руб.")
        self.button = self.ui.button
