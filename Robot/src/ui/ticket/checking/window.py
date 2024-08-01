import base64
import datetime
import sys

import cv2
from aiohttp import ClientSession
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QMainWindow
from qasync import asyncSlot

import ui.ticket.checking.ticket_ui as design
from tickets.service import validate_user_ticket


class TicketCheckingWindow(QMainWindow):
    def __init__(
            self,
            station_id: str,
            train_number: int,
            wagon_number: int,
            date: datetime.datetime,
            session: ClientSession
    ):
        super(TicketCheckingWindow, self).__init__()

        self.station_id = station_id
        self.train_number = train_number
        self.wagon_number = wagon_number
        self.date = date

        self.ui = design.Ui_MainWindow()
        self.ui.setupUi(self)

        self.video_capture = cv2.VideoCapture(0)

        if not self.video_capture.isOpened():
            print("Error: Could not open webcam.")
            sys.exit()

        self.frame_update_timer = QTimer()
        self.frame_update_timer.timeout.connect(self.update_frame)
        self.frame_update_timer.start(30)

        self.face_check_timer = QTimer()
        self.face_check_timer.timeout.connect(self.check)
        self.face_check_timer.start(2000)

        self.session = session
        self.is_working = False

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            self.ui.video_label.setPixmap(QPixmap.fromImage(q_img))

    def closeEvent(self, event):
        self.video_capture.release()
        event.accept()

    @asyncSlot()
    async def check(self):
        if self.is_working:
            return

        _, frame = self.video_capture.read()
        _, frame = cv2.imencode('.jpg', frame)
        im_bytes = frame.tobytes()
        im_b64 = base64.b64encode(im_bytes).decode("utf-8")

        try:
            self.is_working = True

            result = await validate_user_ticket(
                station_id=self.station_id,
                train_number=self.train_number,
                wagon_number=self.wagon_number,
                date=self.date,
                face=im_b64,
                session=self.session
            )
            print("Ticket Check Result:", result)
            self.is_working = False
        except Exception as e:
            print("Ticket Check Error:", e)
            self.is_working = False
