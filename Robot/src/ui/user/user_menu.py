from qasync import asyncSlot

import ui.user.main_menu_ui as main_design
from config import get_config
from fsm.fsm import FSM
from fsm.state import State
from states.destination_info_state import DestinationInfoState
from states.store_category_selection_state import StoreCategorySelectionState
from store.service import get_store
from ui.basic_window import BasicWindow
from users.schemes import User
from users.service import get_user_destination


class UserMenu:
    def __init__(
            self,
            fsm: FSM,
            user: User,
            state: State
    ):
        super(UserMenu, self).__init__()

        self.ui = main_design.Ui_MainWindow()

        self.session = fsm.context["session"]

        self.fsm = fsm
        self.context = fsm.context
        self.user = user
        self.state = state

    def start(self, window: BasicWindow):
        self.ui.setupUi(window)
        self.ui.welcomeLabel.setText(self.ui.welcomeLabel.text().format(self.user.name))

        if "train_number" not in self.context:
            self.ui.pushButton.setEnabled(False)
            self.ui.pushButton_2.setEnabled(False)
        else:
            self.ui.pushButton.setEnabled(True)
            self.ui.pushButton_2.setEnabled(True)

        # self.ui.pushButton.clicked.connect(self.train)
        self.ui.pushButton_2.clicked.connect(self.destination_info)
        self.ui.pushButton.clicked.connect(self.open_store)

    def stop(self):
        pass

    @asyncSlot()
    async def destination_info(self):
        destination = await get_user_destination(
            self.session,
            self.user.id,
            self.context["train_number"],
            self.context["train_start_date"],
        )
        self.fsm.change_state(
            DestinationInfoState(
                destination
            )
        )

    @asyncSlot()
    async def open_store(self):
        # noinspection PyBroadException
        try:
            self.ui.pushButton.setEnabled(False)
            self.ui.pushButton_2.setEnabled(False)

            config = get_config()
            store = await get_store(
                config.DEFAULT_STORE,
                self.session
            )
            self.fsm.context["store"] = store
            self.fsm.change_state(
                StoreCategorySelectionState(
                    store,
                    self.state
                )
            )
        except Exception as e:
            print("Error when try load store: " + str(e))
            self.ui.pushButton.setEnabled(True)
            self.ui.pushButton_2.setEnabled(True)
