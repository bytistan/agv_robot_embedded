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

    def capture_left_frame(self):
        """Capture a single frame from the left camera of the ZED camera."""
        
        left_image = sl.Mat()
        runtime_parameters = sl.RuntimeParameters()
        
        if self.cam.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # Retrieve the left image in grayscale
            self.cam.retrieve_image(left_image, sl.VIEW.LEFT_GRAY)
            left_frame = left_image.get_data()
            return left_frame
        else:
            print("Failed to capture left image")
            return None

    def capture_right_frame(self):
        """Capture a single frame from the right camera of the ZED camera."""
        
        right_image = sl.Mat()
        runtime_parameters = sl.RuntimeParameters()
        
        if self.cam.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # Retrieve the right image in grayscale
            self.cam.retrieve_image(right_image, sl.VIEW.RIGHT_GRAY)
            right_frame = right_image.get_data()
            return right_frame
        else:
            print("Failed to capture right image")
            return None

    def close(self):
        """Close the ZED camera."""

        self.cam.close()
