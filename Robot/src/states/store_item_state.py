from fsm.state import State
from store.schemes import StoreItem
from ui.store.item.window import StoreItemWindow


class StoreItemState(State):
    def __init__(
            self,
            item: StoreItem
    ):
        super().__init__()
        self.service: StoreItemWindow | None = None
        self.item = item

    def start(self, fsm) -> None:
        if self.service is None:
            self.service = StoreItemWindow(
                self.item,
                fsm

            )
        self.service.start(fsm.context["window"])

    def stop(self) -> None:
        self.service.stop()
