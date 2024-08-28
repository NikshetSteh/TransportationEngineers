from fsm.state import State
from ui.store.category_selection.window import StoreCategorySelection


class StoreCategorySelectionState(State):
    def __init__(
            self,
            store_id: str
    ):
        super().__init__()
        self.service: StoreCategorySelection | None = None
        self.store_id = store_id

    def start(self, fsm) -> None:
        if self.service is None:
            self.service = StoreCategorySelection(
                self.store_id,
                fsm

            )
        self.service.start(fsm.context["window"])

    def stop(self) -> None:
        self.service.stop()
