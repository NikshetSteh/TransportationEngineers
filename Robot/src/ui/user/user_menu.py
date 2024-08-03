import ui.user.main_menu_ui as main_design
from fsm.fsm import FSM
from ui.basic_window import BasicWindow
from users.schemes import User


class UserMenu:
    def __init__(
            self,
            fsm: FSM,
            user: User,
    ):
        super(UserMenu, self).__init__()

        self.ui = main_design.Ui_MainWindow()

        self.session = fsm.context["session"]

        self.fms = fsm
        self.user = user

    def start(self, window: BasicWindow):
        self.ui.setupUi(window)
        self.ui.welcomeLabel.setText(self.ui.welcomeLabel.text().format(self.user.name))

    def stop(self):
        pass
