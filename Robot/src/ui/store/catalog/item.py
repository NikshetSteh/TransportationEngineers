import aiohttp
from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget
from qasync import asyncSlot

from config import get_config
from ui.store.catalog.item_ui import Ui_ItemUI as Design


class Item(QWidget):
    trigger = Signal()

    def __init__(self, name: str = "", price_penny: int = 0, parent=None, logo: str = ""):
        super(Item, self).__init__(parent)
        self.ui = Design()
        self.ui.setupUi(self)

        self.trigger.connect(self.load_image)

        self.setMinimumSize(450, 155)
        self.ui.name.setText(name)
        if price_penny % 100 == 0:
            self.ui.price.setText(f"{price_penny // 100} руб.")
        else:
            self.ui.price.setText(f"{price_penny // 100}.{price_penny % 100} руб.")
        self.button = self.ui.button
        self.image_url = logo

        if logo != "":
            self.trigger.emit()

    @asyncSlot()
    async def load_image(self):
        config = get_config()

        async with aiohttp.ClientSession() as session:
            async with session.get(config.RESOURCE_URL + "/static/logos/" + self.image_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)
                    self.ui.label.setPixmap(pixmap)
                else:
                    print(f"Failed to fetch image: {response.status}")
                    return None
