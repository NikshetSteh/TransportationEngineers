import asyncio

from aiohttp import ClientSession
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QVBoxLayout, QWidget
from qasync import asyncSlot

import ui.user.destination_info.destinations_info_list_ui as main_design
from config import get_config
from fsm.fsm import FSM
from info_service.schemes import Attraction, Hotel
from info_service.service import (get_destination_attractions,
                                  get_destination_hotels)
from schemes import Page
from ui.basic_window import BasicWindow
from ui.user.destination_info.item_info_ui import ItemInfoUI

config = get_config()


def process_scroll_area(scroll_area) -> QVBoxLayout:
    scroll_widget = QWidget()
    scroll_layout = QVBoxLayout(scroll_widget)
    scroll_layout.setContentsMargins(0, 0, 0, 0)

    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(scroll_widget)

    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    return scroll_layout


async def load_logo(url: str, session: ClientSession) -> QPixmap:
    async with session.get(config.RESOURCE_URL + url) as response:
        image = QPixmap()
        data = await response.read()
        image.loadFromData(data)
        return image


class UserMenu:
    def __init__(
            self,
            fsm: FSM,
            destination_id: str,
            last_state
    ):
        super(UserMenu, self).__init__()

        self.timer = None
        self.hotels_layout = None
        self.attractions_layout = None

        self.ui = main_design.Ui_MainWindow()

        self.session: ClientSession = fsm.context["session"]
        self.fsm = fsm

        self.destination_id = destination_id
        self.buffer = []
        self.last_state = last_state

    def start(self, window: BasicWindow) -> None:
        self.ui.setupUi(window)

        self.hotels_layout = process_scroll_area(self.ui.scrollArea)
        self.attractions_layout = process_scroll_area(self.ui.scrollArea_2)
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_data)
        self.timer.start(1000)

        self.ui.pushButton.clicked.connect(
            lambda: self.fsm.change_state(self.last_state)
        )

    @asyncSlot()
    async def load_data(self):
        await self.parse_data(
            await get_destination_hotels(self.destination_id, self.session),
            self.hotels_layout
        )
        await self.parse_data(
            await get_destination_attractions(self.destination_id, self.session),
            self.attractions_layout
        )
        self.timer.stop()

    async def parse_data(
            self,
            objects: Page[Hotel] | Page[Attraction],
            layout: QVBoxLayout,
    ):
        tasks = []

        tasks.extend(
            [
                load_logo(i.logo_url, self.session)
                for i in objects.items
            ]
        )

        logos = await asyncio.gather(*tasks, return_exceptions=True)

        for i in range(len(objects.items)):
            item = ItemInfo(
                name=objects.items[i].name,
                image=logos[i],
                description=objects.items[i].description
            )
            layout.addWidget(item)

    def stop(self) -> None:
        pass


class ItemInfo(QWidget):
    def __init__(
            self,
            name: str,
            image: QPixmap,
            description: str
    ):
        margins = 16
        width = 378 - margins * 2

        super(ItemInfo, self).__init__()

        self.ui = ItemInfoUI()
        self.ui.setup_ui(self, width, margins, name, description, image)
