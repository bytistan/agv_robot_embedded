import cv2
from .helper import gstreamer_pipeline

class Camera:
    def __init__(self):
        self.cap = None
        self.open_camera()

    def open_camera(self):
        self.cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open camera!")

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to read frame!")
        return frame

    def close(self):
        self.cap.release()
