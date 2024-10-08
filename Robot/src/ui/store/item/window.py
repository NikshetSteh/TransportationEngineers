from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from qasync import asyncSlot

import ui.store.item.item_ui as main_design
from config import get_config
from fsm.fsm import FSM
from fsm.state import State
from store.schemes import PurchaseItem, StoreItem
from store.service import create_purchase
from ui.basic_window import BasicWindow


class StoreItemWindow:
    def __init__(
            self,
            item: StoreItem,
            fsm: FSM,
            last_state: State
    ):
        self.ui = main_design.Ui_MainWindow()

        self.session = fsm.context["session"]
        self.is_waiting = False

        self.fsm = fsm
        self.item = item
        self.last_state = last_state

        self.timer = QTimer()
        self.timer.timeout.connect(self.load_logo)
        self.timer.start(1)

    def start(self, window: BasicWindow):
        self.ui.setupUi(window)
        self.is_waiting = False

        self.ui.pushButton.clicked.connect(self.return_to_last_state)

        self.ui.name.setText(self.item.name)
        self.ui.description.setText(self.item.description)
        self.ui.count.setText(f"{self.item.balance} шт.")
        self.ui.pushButton_2.clicked.connect(
            self.buy
        )

        if self.item.price_penny % 100 == 0:
            self.ui.price.setText(f"{self.item.price_penny // 100} руб.")
        else:
            self.ui.price.setText(f"{self.item.price_penny // 100}.{self.item.price_penny % 100} руб.")

    def stop(self):
        self.timer.stop()

    def return_to_last_state(self):
        self.fsm.change_state(self.last_state)

    @asyncSlot()
    async def load_logo(self):
        config = get_config()

        async with self.session.get(config.RESOURCE_URL + "/static/logos/items/" + self.item.logo_url) as response:
            if response.status == 200:
                image_data = await response.read()
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                self.ui.icon.setScaledContents(True)
                self.ui.icon.setPixmap(pixmap)
                self.timer.stop()
            else:
                print(f"Failed to fetch image: {response.status}")
                self.timer.stop()

    @asyncSlot()
    async def buy(self):
        await create_purchase(
            self.fsm.context["store"].id,
            self.fsm.context["user"].id,
            [
                PurchaseItem(
                    item_id=self.item.id,
                    count=1
                )
            ],
            True,
            self.session
        )
