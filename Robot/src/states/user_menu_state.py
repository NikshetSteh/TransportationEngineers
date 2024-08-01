from fsm.state import State
from ui.user.user_menu import UserMenu
from users.schemes import User


class UserMenuState(State):
    def __init__(self, user: User):
        super().__init__()
        self.user = user
        self.service = None

    def start(self, fsm) -> None:
        if self.service is None:
            self.service = UserMenu(
                fsm,
                self.user
            )

        self.service.start(fsm.context["window"])

    def stop(self) -> None:
        self.service.stop()
