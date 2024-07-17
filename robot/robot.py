from camera.cam import Camera 
from image_process.line_follower import LineFollower 
from models import *

from .scanner import Scanner 
from .direction import Direction
from .mission import MissionHandler

import cv2 
import time 
from termcolor import colored
import threading 
import traceback

class Robot_:
    def __init__(self):
        self.camera = Camera()
        self.line_follower = LineFollower()
        self.scanner = Scanner() 
        
        self.order = -1  
        self.direction = Direction()

        self.data = {
            "line_status":None,
        }
        
        self.start_time = time.time()
        self.loop_time = None 
        self.interval = 1

        self.status = {
            "start_time":time.strftime("%H.%M", time.localtime(self.start_time)),
            "battery":0,
            "speed":0,
            "tempature":0,
            "load":0,
            "mission_time":0
        }
      
    def stop(self):
        try:
            self.camera.close()
            cv2.destroyAllWindows()
        except Exception as e:
            self.camera.close()
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def setup(self, mission):
        try:
            self.robot = Robot.filter_one(Robot.id > 0) 
            self.connection = Connection.filter_one(Connection.id > 0)

            self.loop_time = time.time()
            self.mission_handler = MissionHandler(mission)
        except Exception as e:
            self.camera.close()
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def run(self, mission):
        self.setup(mission)

        while True:
            try:
                frame = self.camera.capture_frame()

                if frame is None:
                    print(colored("[WARN] Camera is not working.", "yellow", attrs=["bold"]))
                    break

                self.scanner.update(frame)  

                self.data["line_status"] = self.line_follower.controller(frame)

                self.mission_handler.update(self.scanner.data)

                if self.mission_handler.complated:
                    break

            except KeyboardInterrupt:
                self.camera.close()
            except Exception as e:
                self.camera.close()
                error_details = traceback.format_exc()
                print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

        self.stop() 
