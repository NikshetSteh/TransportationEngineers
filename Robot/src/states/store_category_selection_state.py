from fsm.state import State
from store.schemes import Store
from ui.store.category_selection.window import StoreCategorySelection


class StoreCategorySelectionState(State):
    def __init__(
            self,
            store: Store,
            last_state: State
    ):
        super().__init__()
        self.service: StoreCategorySelection | None = None
        self.store = store
        self.last_state = last_state

    def start(self, fsm) -> None:
        if self.service is None:
            self.service = StoreCategorySelection(
                self.store,
                fsm,
                self.last_state,
                self
            )

        self.service.start(fsm.context["window"])

    def stop(self) -> None:
        self.service.stop()
