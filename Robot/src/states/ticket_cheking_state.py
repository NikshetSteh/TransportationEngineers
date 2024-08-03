import datetime

from fsm.fsm import FSM
from fsm.state import State
from ui.ticket.checking.ticket_checking import TicketChecking


class TicketCheckingState(State):
    def __init__(
            self,
            station_id: str,
            train_number: int,
            wagon_number: int,
            date: datetime.datetime
    ) -> None:
        super().__init__()
        self.service = None
        self.station_id = station_id
        self.train_number = train_number
        self.wagon_number = wagon_number
        self.date = date

    def start(self, fsm: FSM) -> None:
        if self.service is None:
            self.service = TicketChecking(
                self.station_id,
                self.train_number,
                self.wagon_number,
                self.date,
                fsm,
                self
            )
        self.service.start(fsm.context["window"])

    def stop(self) -> None:
        self.service.stop()
