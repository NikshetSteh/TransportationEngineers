from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QWidget

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
    def __init__(self):
        self.ui = Ui_MainWindow()

    def start(self, window: BasicWindow):
        self.ui.setupUi(window)

        scroll_area = self.ui.scrollArea

        scroll_layout = process_scroll_area(scroll_area)

        for i in range(10):
            scroll_layout.addWidget(
                Item(),
                i // 2,
                i % 2
            )

    def stop(self):
        pass
