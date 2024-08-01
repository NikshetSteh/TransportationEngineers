import datetime

from aiohttp import ClientSession

from fms.fms import FMS
from fms.state import State
from ui.ticket.checking.ticket_checking_results import TicketCheckingResults
from ui.basic_window import BasicWindow
from tickets.schemes import Ticket


class TicketCheckingResultState(State):
    def __init__(
            self,
            station_id: str,
            train_number: int,
            wagon_number: int,
            date: datetime.datetime,
            session: ClientSession,
            window: BasicWindow,
            last_state: State,
            fms: FMS,
            status: bool,
            ticket: Ticket = None
    ) -> None:
        super().__init__()
        self.window = window
        self.service = TicketCheckingResults(
            station_id,
            train_number,
            wagon_number,
            date,
            session,
            status,
            fms,
            last_state,
            ticket
        )

    def start(self) -> None:
        self.service.start(self.window)

    def stop(self) -> None:
        self.service.stop()
