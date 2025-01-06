import cv2
import numpy as np


class Camera:
    def __init__(self):
        self.cap = None

    def __enter__(self):
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise Exception("Unable to open camera")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cap.release()

    def get_frame(self) -> tuple[bool, np.ndarray]:
        ret, frame = self.cap.read()
        return ret, frame
