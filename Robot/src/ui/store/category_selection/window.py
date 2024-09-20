import ui.store.category_selection.category_select_ui as main_design
from fsm.fsm import FSM
from fsm.state import State
from states.catalog_state import CatalogState
from store.schemes import Store
from ui.basic_window import BasicWindow


class StoreCategorySelection:
    def __init__(
            self,
            store: Store,
            fsm: FSM,
            last_state: State,
            state: State
    ):
        self.ui = main_design.Ui_MainWindow()

        self.session = fsm.context["session"]
        self.is_waiting = False

        self.fsm = fsm
        self.store = store
        self.last_state = last_state
        self.state = state

    def start(self, window: BasicWindow):
        self.ui.setupUi(window)
        self.ui.pushButton.clicked.connect(self.return_to_last_state)
        # TODO: Add recommendations
        self.ui.train_souvenirs.clicked.connect(self.make_go_to_category_handler("train_souvenirs"))
        self.ui.city_souvenirs.clicked.connect(self.make_go_to_category_handler("city_souvenirs"))
        self.ui.food.clicked.connect(self.make_go_to_category_handler("food"))
        self.is_waiting = False

    def stop(self):
        pass

    def return_to_last_state(self):
        self.fsm.change_state(self.last_state)

    def make_go_to_category_handler(self, category: str):
        def handler():
            self.fsm.change_state(
                CatalogState(
                    self.store,
                    category,
                    self.state
                )
            )

        return handler
