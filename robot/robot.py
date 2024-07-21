from camera.cam import Camera 
from image_process.line_follower import LineFollower 
from models import *

from .scanner import Scanner 
from .location import Location_
from .direction import Direction
from .protocol import Protocol 

import cv2 
import time 
from termcolor import colored

import threading 
import traceback

class Robot_:
    def __init__(self):
        self.camera = Camera()
        self.line_follower = LineFollower()
        self.location = Location_()
        self.scanner = Scanner(self.location) 
        self.direction = Direction()

        self.protocol = Protocol(self.direction, self.location)

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
        except Exception as e:
            self.camera.close()
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def setup(self, mission):
        try:
            self.robot = Robot.filter_one(Robot.id > 0) 
            self.connection = Connection.filter_one(Connection.id > 0)

            self.loop_time = time.time()

            self.protocol.setup(mission)  
            self.protocol.guidance.setup(mission)

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
                
                if self.protocol.guidance.complated:
                    break
                
                self.protocol.update(self.data, self.scanner.data)

            except KeyboardInterrupt:
                self.camera.close()
                break 
            except Exception as e:
                self.camera.close()
                error_details = traceback.format_exc()
                print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))
                break

        self.stop() 
