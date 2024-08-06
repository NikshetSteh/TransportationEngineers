import datetime

from aiohttp import ClientSession
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMainWindow

import ui.ticket.checking.ticket_result_s_ui as design_s
import ui.ticket.checking.ticket_result_ui as design_f
from fsm.context import Context
from fsm.fsm import FSM
from fsm.state import State
from tickets.schemes import Ticket
from users.schemes import User


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
            user: User | None = None
    ):
        self.station_id = station_id
        self.train_number = train_number
        self.wagon_number = wagon_number
        self.date = date
        self.user = user

        self.ui = None

        self.auto_close_timer = QTimer()

        self.session: ClientSession = context["session"]

        self.status = status
        self.ticket = ticket

        self.fsm: FSM = context["fsm"]
        self.handle_state = handle_state

    def start(self, window: QMainWindow):
        self.ui = design_s.Ui_MainWindow() if self.status else design_f.Ui_MainWindow()
        self.ui.setupUi(window)

        if self.status:
            self.ui.label_2.setText(
                self.ui.label_2.text().format(self.user.name)
            )
            self.ui.label_3.setText(
                self.ui.label_3.text().format(self.ticket.place_number)
            )
        else:
            self.ui.IconLabel.setPixmap(QPixmap(u":/icons/media/cancel.png"))
            if self.ticket is None:
                self.ui.TextLabel.setText("Wrong Ticket\n\n")
            else:
                self.ui.TextLabel.setText(
                    f"Wrong Ticket\n\n"
                )

        self.auto_close_timer.timeout.connect(self.go_back)
        self.auto_close_timer.start(1000)

    def stop(self):
        self.auto_close_timer.stop()

    def go_back(self):
        self.fsm.change_state(self.handle_state)
