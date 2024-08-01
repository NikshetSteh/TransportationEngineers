import datetime

from aiohttp import ClientSession

from fms.state import State
from ui.ticket.checking.window import TicketCheckingWindow


class TicketCheckingState(State):
    def __init__(
            self,
            station_id: str,
            train_number: int,
            wagon_number: int,
            date: datetime.datetime,
            session: ClientSession
    ) -> None:
        super().__init__()
        self.window = None
        self.station_id = station_id
        self.train_number = train_number
        self.wagon_number = wagon_number
        self.date = date
        self.session = session

    def start(self) -> None:
        self.window = TicketCheckingWindow(
            self.station_id,
            self.train_number,
            self.wagon_number,
            self.date,
            self.session
        )
        self.window.show()

    def stop(self) -> None:
        self.window.close()
