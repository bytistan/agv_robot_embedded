# MIT License
# Copyright (c) 2019 JetsonHacks
# See license for more details

# Description:
# This script uses a CSI camera (such as the Raspberry Pi Version 2) 
# connected to an NVIDIA Jetson Nano Developer Kit using OpenCV.
# Drivers for the camera and OpenCV are included in the base image.

import cv2
import time

try:
    from  Queue import  Queue
except ModuleNotFoundError:
    from  queue import  Queue

import threading
import signal
import sys

from .frame_reader import FrameReader
from .helper import gstreamer_pipeline
from .previewer import Previewer

class Camera(object):
    def __init__(self):
        self.open_camera()

        self.frame_reader = FrameReader(self.cap)
        self.frame_reader.daemon = True
        self.frame_reader.start()

        self.previewer = Previewer(self.frame_reader)

    def open_camera(self):
        self.cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open camera!")

    def getFrame(self):
        return self.frame_reader.getFrame()

    def start_preview(self):
        self.previewer.daemon = True
        self.previewer.start_preview()

    def stop_preview(self):
        self.previewer.stop_preview()
        self.previewer.join()
    
    def close(self):
        self.frame_reader.stop()
        self.cap.release()
