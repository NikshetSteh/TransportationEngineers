from fsm.state import State
from ui.user.destination_info.destination_info import UserMenu


class DestinationInfoState(State):
    def __init__(
            self,
            destination_id: str
    ):
        super().__init__()
        self.service: UserMenu | None = None
        self.destination_id = destination_id

    def start(self, fsm) -> None:
        if self.service is None:
            self.service = UserMenu(
                fsm,
                destination_id=self.destination_id
            )
        self.service.start(fsm.context["window"])

    def stop(self) -> None:
        self.service.stop()
