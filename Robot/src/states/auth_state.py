from fsm.state import State
from ui.auth.auth import Auth


class AuthState(State):
    def __init__(self, next_state: type(State)):
        super().__init__()
        self.next_state = next_state
        self.service: Auth | None = None

    def start(self, fsm) -> None:
        if self.service is None:
            self.service = Auth(
                fsm,
                self,
                self.next_state
            )
        self.service.start(fsm.context["window"])

    def stop(self) -> None:
        self.service.stop()
