import sys
import cv2
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QImage, QPixmap
import Ticket_ui as design
import asyncio
from qasync import QEventLoop, asyncSlot
import base64

class VideoCapture(QMainWindow):
    def __init__(self):
        super(VideoCapture, self).__init__()
        self.ui = design.Ui_MainWindow()
        self.ui.setupUi(self)

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            sys.exit()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.timer_f = QTimer()
        self.timer_f.timeout.connect(self.chek)
        self.timer_f.start(2000)


    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.ui.video_label.setPixmap(QPixmap.fromImage(q_img))

    def closeEvent(self, event):
        self.cap.release()
        event.accept()
        

    @asyncSlot()
    async def chek(self):
        _, frame = self.cap.read()
        _, frame = cv2.imencode('.jpg', frame) 
        im_bytes = frame.tobytes()
        im_b64 = base64.b64encode(im_bytes)
        print(im_b64.decode())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = VideoCapture()
    window.show()

    with loop:
        loop.run_forever() 