import pyzed.sl as sl
import cv2
import numpy as np

class Camera:
    def __init__(self):
        """Initialize the ZED camera with specific settings."""

        self.cam = sl.Camera()
        self.init_params = sl.InitParameters()
        self.init_params.camera_resolution = sl.RESOLUTION.HD720  # Set resolution
        self.init_params.depth_mode = sl.DEPTH_MODE.NONE  # Depth mode is not used
        self.init_params.camera_fps = 30  # Set the camera frame rate to 30 FPS
        self.init_params.camera_image_flip = sl.FLIP_MODE.AUTO  # Automatic image flipping
        self.init_params.coordinate_units = sl.UNIT.METER

        if self.cam.open(self.init_params) != sl.ERROR_CODE.SUCCESS:
            print("Failed to start camera")
            exit(1)

    def capture_frame(self):
        """Capture a single frame from the ZED camera."""
        
        image_zed = sl.Mat()
        runtime_parameters = sl.RuntimeParameters()
        if self.cam.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # Retrieve the image in grayscale
            self.cam.retrieve_image(image_zed, sl.VIEW.LEFT_GRAY)
            frame = image_zed.get_data()
            return frame
        else:
            print("Failed to capture image")
            return None

    def close(self):
        """Close the ZED camera."""

        self.cam.close()
