import base64
import datetime

import cv2
import numpy as np
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap
from qasync import asyncSlot

import ui.ticket.checking.ticket_ui as main_design
from fsm.fsm import FSM
from fsm.state import State
from states.ticket_checking_result_state import TicketCheckingResultState
from tickets.exceptions import InvalidTicket
from tickets.service import validate_user_ticket
from ui.basic_window import BasicWindow
from users.service import get_user_by_id


class TicketChecking:
    def __init__(
            self,
            station_id: str,
            train_number: int,
            wagon_number: int,
            date: datetime.datetime,
            fsm: FSM,
            state: State
    ):
        super(TicketChecking, self).__init__()

        self.camera = None
        self.station_id = station_id
        self.train_number = train_number
        self.wagon_number = wagon_number
        self.date = date

        self.ui = main_design.Ui_MainWindow()

        self.session = fsm.context["session"]
        self.is_waiting = False

        self.frame_update_timer = None
        self.face_check_timer = None

        self.fsm = fsm
        self.state = state
        self.window = None

    def update_frame(self):
        ret, frame = self.camera.get_frame()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.ascontiguousarray(frame[:, 84:84+476])
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            self.ui.video_label.setPixmap(QPixmap.fromImage(q_img))

    def start(self, window: BasicWindow):
        self.ui.setupUi(window)

        self.frame_update_timer = QTimer()
        self.frame_update_timer.timeout.connect(self.update_frame)
        self.frame_update_timer.start(30)

        self.face_check_timer = QTimer()
        self.face_check_timer.timeout.connect(self.check)
        self.face_check_timer.start(2000)

        self.window = window

        self.camera = self.fsm.context["camera"]

        self.is_waiting = False

    def stop(self):
        self.frame_update_timer.stop()
        self.face_check_timer.stop()

    @asyncSlot()
    async def check(self):
        if self.is_waiting:
            return

        _, frame = self.camera.get_frame()
        # frame = cv2.imread("t/a.jpg")
        frame = np.ascontiguousarray(frame[:, 84:84 + 476])
        _, frame = cv2.imencode('.jpg', frame)
        im_bytes = frame.tobytes()
        im_b64 = base64.b64encode(im_bytes).decode("utf-8")

        status = False
        ticket = None
        user = None
        ready = False

        try:
            self.is_waiting = True

            ticket = await validate_user_ticket(
                station_id=self.station_id,
                train_number=self.train_number,
                wagon_number=self.wagon_number,
                date=self.date,
                face=im_b64,
                session=self.session
            )
            status = True
            ready = True
        except InvalidTicket as ticket_exception:
            ticket = ticket_exception.right_ticket
            status = False
            ready = True
        except Exception as e:
            print("Ticket Check Error:", e)
            self.is_waiting = False

        if ticket is not None:
            user = await get_user_by_id(ticket.user_id, self.session)

        if ready:
            self.fsm.change_state(
                TicketCheckingResultState(
                    station_id=self.station_id,
                    train_number=self.train_number,
                    wagon_number=self.wagon_number,
                    date=self.date,
                    handle_state=self.state,
                    status=status,
                    ticket=ticket,
                    user=user
                )
            )
