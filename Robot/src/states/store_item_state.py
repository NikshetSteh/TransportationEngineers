from fsm.state import State
from store.schemes import StoreItem
from ui.store.item.window import StoreItemWindow


class StoreItemState(State):
    def __init__(
            self,
            item: StoreItem,
            last_state: State
    ):
        super().__init__()
        self.service: StoreItemWindow | None = None
        self.item = item
        self.last_state: State = last_state

    def start(self, fsm) -> None:
        if self.service is None:
            self.service = StoreItemWindow(
                self.item,
                fsm,
                self.last_state
            )
        self.service.start(fsm.context["window"])

    def stop(self) -> None:
        self.service.stop()
