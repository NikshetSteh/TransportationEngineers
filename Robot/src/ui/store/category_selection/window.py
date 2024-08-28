import ui.store.category_selection.category_select_ui as main_design
from fsm.fsm import FSM
from ui.basic_window import BasicWindow


class StoreCategorySelection:
    def __init__(
            self,
            store_id: str,
            fsm: FSM
    ):
        self.ui = main_design.Ui_MainWindow()

        self.session = fsm.context["session"]
        self.is_waiting = False

        self.fsm = fsm
        self.store_id = store_id

    def start(self, window: BasicWindow):
        self.ui.setupUi(window)
        self.is_waiting = False

    def stop(self):
        pass
