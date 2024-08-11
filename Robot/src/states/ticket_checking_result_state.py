import datetime

from fsm.fsm import FSM
from fsm.state import State
from tickets.schemes import Ticket
from ui.ticket.checking.ticket_checking_results import TicketCheckingResults
from users.schemes import User


class TicketCheckingResultState(State):
    def __init__(
            self,
            station_id: str,
            train_number: int,
            wagon_number: int,
            date: datetime.datetime,
            handle_state: State,
            status: bool,
            ticket: Ticket = None,
            user: User = None
    ) -> None:
        super().__init__()
        self.service = None
        self.station_id = station_id
        self.train_number = train_number
        self.wagon_number = wagon_number
        self.date = date
        self.handle_state = handle_state
        self.status = status
        self.ticket = ticket
        self.user = user

    def start(self, fsm: FSM) -> None:
        if self.service is None:
            self.service = TicketCheckingResults(
                fsm.context,
                self.station_id,
                self.train_number,
                self.wagon_number,
                self.date,
                self.status,
                self.handle_state,
                self.ticket,
                self.user
            )
        self.service.start(fsm.context["window"])

    def stop(self) -> None:
        self.service.stop()
