from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QWidget

from fsm.fsm import FSM
from fsm.state import State
from states.store_item_state import StoreItemState
from store.schemes import Store, StoreItem
from ui.basic_window import BasicWindow
from ui.store.catalog.catalog_ui import Ui_MainWindow
from ui.store.catalog.item import Item


def process_scroll_area(scroll_area) -> QGridLayout:
    scroll_widget = QWidget()
    scroll_layout = QGridLayout(scroll_widget)
    scroll_layout.setContentsMargins(0, 0, 0, 0)

    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(scroll_widget)

    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    return scroll_layout


class Catalog:
    def __init__(
            self,
            store: Store,
            category: str,
            last_state: State,
            fsm: FSM,
            state: State
    ):
        self.ui = Ui_MainWindow()
        self.store = store
        self.fsm = fsm
        self.last_state = last_state
        self.category = category
        self.state = state

        self.items = [
            i for i in store.items if i.category == category
        ]

    def start(self, window: BasicWindow):
        self.ui.setupUi(window)

        self.ui.pushButton.clicked.connect(self.return_to_last_state)

        scroll_area = self.ui.scrollArea

        scroll_layout = process_scroll_area(scroll_area)

        for i in range(len(self.items)):
            item = Item(
                name=self.items[i].name,
                price_penny=self.items[i].price_penny,
                logo=self.items[i].logo_url
            )
            scroll_layout.addWidget(
                item,
                i // 2,
                i % 2
            )
            item.button.clicked.connect(
                lambda: self.open_item(self.items[i])
            )

    def stop(self):
        pass

    def return_to_last_state(self):
        self.fsm.change_state(self.last_state)

    def open_item(self, item: StoreItem):
        self.fsm.change_state(
            StoreItemState(
                item,
                self.state
            )
        )
