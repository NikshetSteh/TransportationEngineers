from fsm.state import State
from store.schemes import Store
from ui.store.catalog.catalog import Catalog


class CatalogState(State):
    def __init__(
            self,
            store: Store,
            category: str,
            last_state: State
    ):
        super().__init__()
        self.service: Catalog | None = None
        self.store = store
        self.category = category
        self.last_state = last_state

    def start(self, fsm) -> None:
        if self.service is None:
            self.service = Catalog(
                self.store,
                self.category,
                self.last_state,
                fsm,
                self
            )
        self.service.start(fsm.context["window"])

    def stop(self) -> None:
        self.service.stop()
