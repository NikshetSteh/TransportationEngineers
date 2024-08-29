import ui.store.item.item_ui as main_design
from fsm.fsm import FSM
from store.schemes import StoreItem
from ui.basic_window import BasicWindow


class StoreItemWindow:
    def __init__(
            self,
            item: StoreItem,
            fsm: FSM
    ):
        self.ui = main_design.Ui_MainWindow()

        self.session = fsm.context["session"]
        self.is_waiting = False

        self.fsm = fsm
        self.item = item

    def start(self, window: BasicWindow):
        self.ui.setupUi(window)
        self.is_waiting = False

        self.ui.name.setText(self.item.name)
        self.ui.description.setText(self.item.description)
        self.ui.count.setText(f"{self.item.balance} шт.")

        if self.item.price_penny % 100 == 0:
            self.ui.price.setText(f"{self.item.price_penny // 100} руб.")
        else:
            self.ui.price.setText(f"{self.item.price_penny // 100}.{self.item.price_penny % 100} руб.")

    def stop(self):
        pass
