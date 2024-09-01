from fsm.state import State
from ui.store.catalog.catalog import Catalog


class CatalogState(State):
    def __init__(
            self
    ):
        super().__init__()
        self.service: Catalog | None = None

    def start(self, fsm) -> None:
        if self.service is None:
            self.service = Catalog(

            )
        self.service.start(fsm.context["window"])

    def stop(self) -> None:
        self.service.stop()
