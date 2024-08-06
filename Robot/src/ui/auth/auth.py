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
            next_state: type(State)
    ):
        super(Auth, self).__init__()

        self.ui = main_design.Ui_MainWindow()

        self.camera = None

        self.session = fsm.context["session"]
        self.is_waiting = False

        self.frame_update_timer = None
        self.face_check_timer = None

        self.fsm = fsm
        self.state = state

        self.next_state = next_state

    def update_frame(self):
        ret, frame = self.camera.get_frame()
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
        _, frame = cv2.imencode('.jpg', frame)
        im_bytes = frame.tobytes()
        im_b64 = base64.b64encode(im_bytes).decode("utf-8")

        result = await indentify_face(
            face=im_b64,
            session=self.session
        )

        if result is not None:
            self.fsm.context["user"] = result
            self.fsm.change_state(self.next_state())
