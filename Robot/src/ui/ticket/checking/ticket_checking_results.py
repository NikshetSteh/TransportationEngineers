import datetime

from aiohttp import ClientSession
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMainWindow

import ui.ticket.checking.ticket_result_ui as design
from fsm.context import Context
from fsm.fsm import FSM
from fsm.state import State
from tickets.schemes import Ticket


class TicketCheckingResults:
    def __init__(
            self,
            context: Context,
            station_id: str,
            train_number: int,
            wagon_number: int,
            date: datetime.datetime,
            status: bool,
            handle_state: State,
            ticket: Ticket | None = None,
    ):
        self.station_id = station_id
        self.train_number = train_number
        self.wagon_number = wagon_number
        self.date = date

        self.ui = design.Ui_MainWindow()

        self.auto_close_timer = QTimer()

        self.session: ClientSession = context["session"]

        self.status = status
        self.ticket = ticket

        self.fsm: FSM = context["fsm"]
        self.handle_state = handle_state

    def start(self, window: QMainWindow):
        self.ui.setupUi(window)

        if self.status:
            self.ui.IconLabel.setPixmap(QPixmap(u":/icons/media/check.png"))
            self.ui.TextLabel.setText(f"Right Ticket\n\nPlace: {self.ticket.place_number}")
        else:
            self.ui.IconLabel.setPixmap(QPixmap(u":/icons/media/cancel.png"))
            if self.ticket is None:
                self.ui.TextLabel.setText("Wrong Ticket\n\n")
            else:
                self.ui.TextLabel.setText(
                    f"Wrong Ticket\n\n"
                    # f"Perhaps you meant:\n\n"
                    # f"- Station: {self.ticket.station_id}\n"
                    # f"- Train: {self.ticket.train_number}\n"
                    # f"- Wagon: {self.ticket.wagon_number}\n"
                    # f"- Place : {self.ticket.place_number}\n"
                    # f"- Date  : {self.ticket.date}"
                )

        self.auto_close_timer.timeout.connect(self.go_back)
        self.auto_close_timer.start(1000)

    def stop(self):
        self.auto_close_timer.stop()

    def go_back(self):
        self.fsm.change_state(self.handle_state)
