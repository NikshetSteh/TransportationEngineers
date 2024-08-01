import base64

import cv2
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap
from qasync import asyncSlot

import ui.auth.auth_ui as main_design
from fsm.fsm import FSM
from fsm.state import State
from ui.basic_window import BasicWindow
from users.service import indentify_face


class Auth:
    def __init__(
            self,
            fsm: FSM,
            state: State,
            next_state: State
    ):
        super(Auth, self).__init__()

        self.ui = main_design.Ui_MainWindow()

        self.video_capture = None

        self.session = fsm.context["session"]
        self.is_waiting = False

        self.frame_update_timer = None
        self.face_check_timer = None

        self.fms = fsm
        self.state = state
        self.window = None

        self.next_state = next_state

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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

        self.video_capture = cv2.VideoCapture(0)

        if not self.video_capture.isOpened():
            print("Error: Could not open webcam.")

        self.is_waiting = False

    def stop(self):
        self.video_capture.release()
        self.frame_update_timer.stop()
        self.face_check_timer.stop()

    @asyncSlot()
    async def check(self):
        if self.is_waiting:
            return

        _, frame = self.video_capture.read()
        _, frame = cv2.imencode('.jpg', frame)
        im_bytes = frame.tobytes()
        im_b64 = base64.b64encode(im_bytes).decode("utf-8")

        result = await indentify_face(
            face=im_b64,
            session=self.session
        )

        if result is not None:
            print(result)

    def restart(self) -> None:
        self.is_waiting = False
