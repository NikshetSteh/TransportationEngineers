from fsm.state import State
from ui.user.user_menu import UserMenu


class UserMenuState(State):
    def __init__(self):
        super().__init__()
        self.service = None

    def start(self, fsm) -> None:
        if self.service is None:
            self.service = UserMenu(
                fsm,
                fsm.context["user"]
            )

        self.service.start(fsm.context["window"])

    def stop(self) -> None:
        self.service.stop()
