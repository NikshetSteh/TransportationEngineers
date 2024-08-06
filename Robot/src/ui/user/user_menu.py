from qasync import asyncSlot

import ui.user.main_menu_ui as main_design
from fsm.fsm import FSM
from states.destination_info_state import DestinationInfoState
from ui.basic_window import BasicWindow
from users.schemes import User
from users.service import get_user_destination


class UserMenu:
    def __init__(
            self,
            fsm: FSM,
            user: User,
    ):
        super(UserMenu, self).__init__()

        self.ui = main_design.Ui_MainWindow()

        self.session = fsm.context["session"]

        self.fsm = fsm
        self.context = fsm.context
        self.user = user

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
